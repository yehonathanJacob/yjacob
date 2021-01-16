import os.path
import logging
import gzip

from dicomaizer.series import SeriesUID
from dicomaizer.common.uid import string2hash
from dicomaizer.exceptions.exceptions import NoImageOrientationError, NoImagePositionError
from dicomaizer.imageplane.orientation_utils import PLANES, AXIAL, get_orientation_vector_for_plane_name
from dicomaizer.imageplane.position_utils import get_image_z_position_or_default
from utils import common
from  dicomaizer.series.series_builder import SeriesBuilder
import dicom
from dicomaizer.imageplane import position_utils, get_plane

logger = logging.getLogger(__name__)


class Scan:
    """ scan master class that handles all volume scans operations from
          loading, handling masks and more sophisticated ( such as brain and
          normalization )"""

    def __init__(self, volume=None):
        self.uid = ''
        self.directory = ''
        self.compressed_volume_directory = None
        self.volume = volume or []  # the CT scan volume
        self.name = ''  # patient name or number
        self.patient_id = ''
        self.date = ''  # scan date
        self.time = ''
        self.metadata = []
        self.size = None
        self.volume_compressed = False
        self.is_simulated_short = False
        self.image_positions = []
        self.plane = None

    @classmethod
    def fromID(cls, uid, scanfolder='', read_volume=True, prefer_compressed_volume=True,
               compressed_volumes_dir=None):
        series_uid = SeriesUID(uid)
        scan = cls()
        scan_dir = os.path.join(scanfolder, series_uid.dicom_dir_name)

        if not os.path.isdir(scan_dir):
            scan_dir = os.path.join(scanfolder, series_uid.optimized_dicom_dir_name)
            if not os.path.isdir(scan_dir):
                raise IOError("Could not find dicom dir " + scan_dir)

        series_builder = SeriesBuilder(uid)

        slices = 0
        for f in os.listdir(scan_dir):
            ds = dicom.read_file(os.path.join(scan_dir, f), force=True, stop_before_pixels=not read_volume)
            z_pos = get_image_z_position_or_default(ds)
            scan.image_positions.append(z_pos)
            if read_volume:
                series_builder.add_slice(dicom.read_file(os.path.join(scan_dir, f)), override_z_pos=z_pos)
            slices += 1

        scan.size = [slices, ds.Rows, ds.Columns]

        scan.uid = uid
        scan.directory = scanfolder
        scan.compressed_volume_directory = compressed_volumes_dir or scanfolder
        scan.name = str(ds.PatientName)
        scan.metadata = _read_metadata(ds)
        scan.body_part = _get_body_part(ds)
        if 'ImageOrientationPatient' in scan.metadata:
            scan.plane = get_plane(scan.metadata['ImageOrientationPatient'])
            scan.image_orientation = scan.metadata['ImageOrientationPatient']
        elif slices == 1:
            scan.image_orientation = get_orientation_vector_for_plane_name(AXIAL)
            scan.plane = get_plane(scan.image_orientation)
        else:
            raise NoImageOrientationError()
        scan.date = scan.metadata['StudyDate']
        scan.time = scan.metadata['StudyTime']
        scan.patient_id = scan.metadata['PatientID'] if 'PatientID' in scan.metadata else ''

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
                ignore_missing_orientation = False
                if slices == 1:
                    ignore_missing_orientation = True
                series = series_builder.build(ignore_missing_orientation=ignore_missing_orientation)

                scan.volume = series.volume
                scan.volume_compressed = False

        return scan

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


def _read_metadata(ds):
    metadata = {}
    metadata['PhotometricInterpretation'] = ds.PhotometricInterpretation

    if 'AccessionNumber' in ds:
        metadata['AccessionNumber'] = ds.AccessionNumber

    if 'StudyInstanceUID' in ds:
        metadata['StudyInstanceUID'] = ds.StudyInstanceUID

    if 'RescaleSlope' in ds:
        metadata['RescaleSlope'] = 1

    if 'RescaleIntercept' in ds:
        metadata['RescaleIntercept'] = 0

    if 'PixelSpacing' in ds:
        metadata['PixelSpacing'] = ds.PixelSpacing[0]

    if 'SliceThickness' in ds:
        metadata['SliceThickness'] = ds.SliceThickness

    if 'ImageOrientationPatient' in ds:
        metadata['ImageOrientationPatient'] = ds.ImageOrientationPatient

    if 'ImagePositionPatient' in ds:
        metadata['ImagePositionPatient'] = ds.ImagePositionPatient

    if 'FrameOfReferenceUID' in ds:
        metadata['FrameOfReferenceUID'] = ds.FrameOfReferenceUID

    if 'StudyDate' in ds:
        metadata['StudyDate'] = ds.StudyDate

    if 'StudyTime' in ds:
        metadata['StudyTime'] = ds.StudyTime

    if 'PatientID' in ds:
        metadata['PatientID'] = ds.PatientID

    return metadata


def _get_body_part(ds):
    if 'Modality' in ds and ds.Modality == 'CR':
        return 'xray_ap'
    return 'uknown_dicom'
