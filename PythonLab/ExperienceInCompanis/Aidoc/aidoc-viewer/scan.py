import os.path
import logging
import numpy as np
import gzip
from utils import common
import h5py

from dicomaizer.series import SeriesUID
from dicomaizer.common.uid import string2hash

import dicom_scan
logger = logging.getLogger(__name__)


class Scan:
    """ scan master class that handles all volume scans operations from
          loading, handeling masks and more sophisticated ( such as brain and
          normalization )"""
    def __init__(self, volume=None):
        self.uid = ''
        self.directory = ''
        self.compressed_volume_directory = None
        self.volume = volume or []  # the CT scan volume
        self.path = []
        self.name = []  # patient name or number
        self.patient_id = ''
        self.date = []  # scan date
        self.time = []
        self.modality = []
        self.defWindow = []  # default viewing window
        self.masks = []
        self.extradata = []  # costum saved user data
        self.metadata = []
        self.roiTexts = []
        self.size = None
        self.volume_compressed = False
        # self.__init__()
        # Read data

    @classmethod
    def fromID(cls, uid, scanfolder='', read_volume=True, prefer_compressed_volume=True,
               compressed_volumes_dir=None):
        series_uid = SeriesUID(uid)
        if len(scanfolder) == 0:
            scanfolder = common.getTMpath('CTscans')

        filename = os.path.join(scanfolder, series_uid.mat_filename)
        if not os.path.isfile(filename):
            return dicom_scan.Scan.fromID(uid, scanfolder, read_volume, prefer_compressed_volume,
                                          compressed_volumes_dir)

        rawScan = h5py.File(filename)

        if 'volume' not in rawScan:
            raise IOError("Invalid scan in file " + filename)

        scan = cls()
        scan.uid = uid
        scan.directory = scanfolder
        scan.compressed_volume_directory = compressed_volumes_dir or scanfolder
        scan.name = rawScan['name'].value.tostring().decode('utf-16')
        scan.defWindow = rawScan['defWindow'].value
        scan.normWindow = rawScan['defWindow'].value + rawScan['matlabWindowShift'].value
        scan.metadata = _read_metadata(rawScan, rawScan['metadata'])
        scan.body_part = _get_scan_type(rawScan)
        try:
            scan.plane = _get_plane(rawScan)
        except Exception as e:
            if scan.body_part == 'brain':
                # We can assume the scan is axial
                logger.warning('uid %s: %s - assuming Axial', uid, str(e))
                scan.plane = 'axial'
            else:
                raise e

        scan.image_orientation = scan.metadata['ImageOrientationPatient'].tolist()
        scan.date = scan.metadata['StudyDate']
        scan.time = scan.metadata['StudyTime']
        scan.patient_id = scan.metadata['PatientID'] if 'PatientID' in scan.metadata else ''

        if 'size' not in rawScan:
            logger.warning('CTscan is missing the "size" field - computing from volume')
            # Volume shape is read as (slice, columns, rows). We want to reorder it to (slice, rows, columns)
            scan.size = rawScan['volume'].shape
            scan.size = [scan.size[0], scan.size[2], scan.size[1]]
        else:
            # The size is read as (rows, columns, slices). To match the volume, we change it to (slices, rows, colums)
            scan.size = rawScan['size'].value.flatten().astype(np.uint16)
            scan.size = [scan.size[2], scan.size[0], scan.size[1]]

        try:
            scan.image_positions = _read_image_positions(rawScan, scan.size[0], scan.plane)
        except Exception as e:
            logger.warning('uid %s: %s', uid, str(e))
            scan.image_positions = []

        if read_volume:
            scan.volume = None
            compressed_volume_file = os.path.join(scan.compressed_volume_directory, string2hash(uid) + '.dat.gz')
            if prefer_compressed_volume and os.path.isfile(compressed_volume_file):
                try:
                    with open(compressed_volume_file, 'rb') as f:
                        scan.volume = f.read()
                    scan.volume_compressed = True
                except Exception:
                    logger.exception('uid %s: Error reading compressed volume', uid)

            if not scan.volume:
                scan.volume = rawScan['volume']
                # Volume shape is read as (slice, columns, rows). We want to reorder it to (slice, rows, columns)
                scan.volume = np.transpose(scan.volume, (0, 2, 1))
                scan.volume_compressed = False

        return scan

    def getMask(self , idx):
        if idx < len(self.masks):
            return self.masks[idx]
        return []

    def getActiveMasks(self):
        activeMasks = []
        for i in range(len(self.masks)):
            if self.masks[i] != []:
                activeMasks.append(i)
        return activeMasks

    def is_color_image(self):
        photometric_interpretation = self.metadata['PhotometricInterpretation'].upper()
        return (photometric_interpretation in ['RGB', 'PALETTE COLOR', 'YBR_FULL', 'YBR_FULL_422', 'YBR_PARTIAL_422',
                                               'YBR_PARTIAL_420', 'YBR_RCT', 'YBR_ICT'])

    def store_compressed_volume(self):
        if len(self.volume) == 0 or self.volume_compressed:
            return

        volume = self.volume

        compressed_volume_file = os.path.join(self.compressed_volume_directory, string2hash(self.uid) + '.dat.gz')
        with open(compressed_volume_file, 'wb') as f:
            gzip_file = gzip.GzipFile(mode='wb', fileobj=f, compresslevel=9)
            gzip_file.write(volume.tobytes())
            gzip_file.close()


def _read_metadata(rawScan, rawMetadata):
    metadata = {}
    metadataKeys = rawMetadata.keys()
    extraData = rawScan['extraData']
    metadata['PhotometricInterpretation'] = rawMetadata['PhotometricInterpretation'].value.tostring().decode('utf-16')

    if 'AN' in extraData and extraData['AN']:
        metadata['AccessionNumber'] = _get_hdf5_string(extraData['AN'])
    elif 'AccessionNumber' in metadataKeys:
        metadata['AccessionNumber'] = _get_hdf5_string(rawMetadata['AccessionNumber'])

    if 'StudyInstanceUID' in metadataKeys:
        metadata['StudyInstanceUID'] = _get_hdf5_string(rawMetadata['StudyInstanceUID'])

    if 'RescaleSlope' in metadataKeys:
        metadata['RescaleSlope'] = np.asscalar(rawMetadata['RescaleSlope'].value)

    if 'RescaleIntercept' in metadataKeys:
        metadata['RescaleIntercept'] = np.asscalar(rawMetadata['RescaleIntercept'].value)

    if 'PixelSpacing' in metadataKeys:
        metadata['PixelSpacing'] = rawMetadata['PixelSpacing'].value[0]

    if 'SliceThickness' in metadataKeys:
        metadata['SliceThickness'] = np.asscalar(rawMetadata['SliceThickness'].value)

    if 'SpacingBetweenSlices' in metadataKeys:
        metadata['SpacingBetweenSlices'] = np.asscalar(rawMetadata['SpacingBetweenSlices'].value)

    if 'ImageOrientationPatient' in metadataKeys:
        metadata['ImageOrientationPatient'] = rawMetadata['ImageOrientationPatient'].value[0]

    if 'ImagePositionPatient' in metadataKeys:
        metadata['ImagePositionPatient'] = rawMetadata['ImagePositionPatient'].value[0]

    if 'FrameOfReferenceUID' in metadataKeys:
        metadata['FrameOfReferenceUID'] = _get_hdf5_string(rawMetadata['FrameOfReferenceUID'])

    if 'StudyDate' in metadataKeys:
        metadata['StudyDate'] = _get_hdf5_string(rawMetadata['StudyDate'])

    if 'StudyTime' in metadataKeys:
        metadata['StudyTime'] = _get_hdf5_string(rawMetadata['StudyTime'])

    if 'PatientID' in metadataKeys:
        metadata['PatientID'] = _get_hdf5_string(rawMetadata['PatientID'])

    return metadata


def _get_hdf5_string(hdf5_element):
    char_array = hdf5_element.value
    if np.max(char_array) < 20:
        return ''
    else:
        return char_array.tostring().decode('utf-16')


def _get_scan_type(rawScan):
    if 'type' in rawScan['extraData']:
        scan_types = _parse_cell_of_strings(rawScan['extraData'], 'type', rawScan)
        if 'hemo' in scan_types:
            return 'brain'
        elif 'cspine' in scan_types:
            return 'cspine'
        elif 'tspine' in scan_types:
            return 'tspine'
        elif 'lspine' in scan_types:
            return 'lspine'
        elif 'chest' in scan_types:
            return 'chest'
        elif 'thorax' in scan_types:
            return 'thorax'
        elif 'abdomen' in scan_types:
            return 'abdomen'
        elif 'pe' in scan_types:
            return 'pe'
        elif 'ctaHead' in scan_types:
            return 'cta_head'
        elif 'xray_ap' in scan_types:
            return 'xray_ap'
        elif 'pn' in scan_types:
            return 'pulmonary_nodules'
        elif 'bl' in scan_types:
            return 'bone_lesion'
        else:
            logger.warning('Unsupported scan type: %s - assuming hemo', str(scan_types))
            return 'brain'
    else:
        logger.warning('Missing scan type - assuming hemo')
        return 'brain'


def _get_plane(rawScan):
    if 'plane' in rawScan['extraData']:
        plane = _get_hdf5_string(rawScan['extraData']['plane'])
        if 'ax' in plane:
            return 'axial'
        elif 'sag' in plane:
            return 'sagittal'
        elif 'cor' in plane:
            return 'coronal'
        else:
            raise Exception('Unsupported plane: ' + plane)
    else:
        raise Exception('Missing scan plane')


def _parse_cell_of_strings(dataset, key, rawScan):
    values = []
    for text_cell in dataset[key]:
        if isinstance(text_cell.item(), int):     # Happens when the key contains an empty cell array
            return parse_single(dataset, key)
        else:
            decoded = _get_hdf5_string(rawScan[text_cell.item()])
            values.append(decoded)
    return values


def parse_single(dataset, key):
    decoded = ''
    for text_cell in dataset[key]:
        try:
            decoded += chr(text_cell.item())
        except:
            return []

    return [decoded]


def _is_empty_metadata(metadata_obj):

    if isinstance(metadata_obj, h5py._hl.group.Group) and len(metadata_obj)>0:
        return False
    if isinstance(metadata_obj, h5py._hl.dataset.Dataset):
        l = metadata_obj.size
        for i in range(l):
            if not metadata_obj[i] == 0:
                return False
    else:
        raise Exception('Unknown type of all_metadata field')
    return True


def _read_image_positions(rawScan, num_slices, plane):
    image_positions = []

    if 'all_metadata' in rawScan and not (_is_empty_metadata(rawScan['all_metadata'])):
        all_metadata = rawScan['all_metadata']
        image_positions_refs = all_metadata['ImagePositionPatient']
        for ref in image_positions_refs:
            image_position = rawScan[ref[0]].value[0]
            image_positions.append(image_position.tolist())
    else:
        first_slice_metadata = _read_metadata(rawScan, rawScan['metadata'])
        if 'SpacingBetweenSlices' not in first_slice_metadata:
            raise Exception('Cannot obtain image position patient info for all slices')

        # Try to guess the image positions for all slices by using SpacingBetweenSlices
        # Note that this isn't accurate and might not even be correct since SpacingBetweenSlices is unreliable
        # TODO: Try to use the first and last slices' metadata to get a more accurate image position
        slice_spacing = first_slice_metadata['SpacingBetweenSlices']
        first_slice_position = np.array(first_slice_metadata['ImagePositionPatient'])

        if plane == 'axial':
            z_idx = 2
        elif plane == 'sagittal':
            z_idx = 0
        elif plane == 'coronal':
            z_idx = 1
        else:
            raise Exception('Unknown orientation: ' + plane)

        for i in np.arange(num_slices):
            slice_position = np.array(first_slice_position)
            slice_position[z_idx] += i * slice_spacing
            image_positions.append(slice_position)

    # if 'lastSliceInfo' not in rawScan['metadata']:
    #     raise Exception('Cannot obtain image position patient info for all slices')
    #
    # logger.warning('CTscan is missing the "all_metadata" field - trying to reconstruct image position patient for '
    #                'all slices')
    #
    # first_slice_metadata = _read_metadata(rawScan, rawScan['metadata'])
    # last_slice_metadata = _read_metadata(rawScan, rawScan['metadata']['lastSliceInfo'])
    # first_slice_position = first_slice_metadata['ImagePositionPatient']
    # last_slice_position = last_slice_metadata['ImagePositionPatient']
    # interpolated_positions = []
    # for i in range(3):
    #     interpolated_positions.append(np.linspace(first_slice_position[i], last_slice_position[i], num=num_slices))
    # image_positions = np.transpose(interpolated_positions, (1, 0))

    return image_positions
