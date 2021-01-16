import logging
from datetime import datetime

from flask import Blueprint, request, abort
from flask.json import jsonify

from werkzeug.datastructures import Headers

from scan import Scan
from models import models
from utils import reports
from utils.testing_envitonment.init_app import app, scan_compressor

data_urls = Blueprint('data_urls', __name__)

@data_urls.route('/scan/<uid>/volume')
def get_scan_volume(uid):
    logging.info("Started at: {}".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
    try:
        accept_encoding = request.headers.get('Accept-Encoding', '')
        prefer_compressed_volume = 'gzip' in accept_encoding.lower()
        scan = Scan.fromID(uid, app.config['CT_SCANS_DIR'], prefer_compressed_volume=prefer_compressed_volume,
                           compressed_volumes_dir=app.config['COMPRESSED_VOLUMES_DIR'])
        logging.info("Got scan: {}".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
        if not scan.volume_compressed:
            if prefer_compressed_volume:
                # compress asynchronously the scan so that next time will be faster
                app.logger.info('No compressed scan was found for %s, compressing...', uid)
                scan_compressor.compress(uid)
            volume = scan.volume.tobytes()
        else:
            volume = scan.volume
        logging.info("Got volume: {}".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
        headers = Headers()
        headers['Content-Length'] = len(volume)
        if scan.volume_compressed:
            headers['Content-Encoding'] = 'gzip'
            headers['Vary'] = 'Accept-Encoding'
        rv = app.response_class(volume, mimetype='application/octet-stream', headers=headers)
        # TODO: Add etag support

        logging.info("Return at: {}".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
        return rv
    except IOError:
        app.logger.warning('Cannot find scan with id %s', uid)
        abort(404)


@data_urls.route('/study/<work_item_id>')
def get_study_metadata(work_item_id):
    try:
        # work_item = get_work_item(uid)
        work_item = get_work_item(work_item_id)
        study_metadata = {
            'uid': work_item.uid,
            'accessionNumber': work_item.accession_number,
            'patientName': work_item.patient_name,
            'patientLocation': work_item.get_patient_location(),
            'series': {}
        }

        for series in work_item.series:
            scan = Scan.fromID(series.uid, app.config['CT_SCANS_DIR'], read_volume=False)
            if work_item.body_part is not None:
                scan.body_part = work_item.body_part
            study_metadata['series'][series.id] = scan_metadata_to_json(scan)

            # check if the study has a report
        report_loader = reports.ReportsLoader(app.config['REPORTS_DIR'])
        report = report_loader.load_report(work_item.accession_number)

        study_metadata['report'] = report

        return jsonify(study_metadata)
    except IOError:
        app.logger.warning('Cannot find scan with work_item_id %s', work_item_id)
        abort(404)


def get_work_item(work_item_id):
    return models.WorkItem.query.filter(models.WorkItem.id.is_(work_item_id)).one()


def scan_metadata_to_json(scan):
    shape = scan.size
    slices = shape[0]
    window_defs = app.config['DEFAULT_WINDOW_DEFS']
    if scan.body_part in window_defs:
        window = window_defs[scan.body_part]
    else:
        logging.warning('Unknown body part "%s" - using default brain window', scan.body_part)
        window = [35, 80]

    # TODO: sent bits allocated to the client so it can calculated the scan size in bytes
    return dict(
        uid=scan.uid,
        accessionNumber=scan.metadata.get('AccessionNumber', scan.uid),
        patientName=scan.name,
        bodyPart=scan.body_part,
        plane=scan.plane,
        slope=scan.metadata.get('RescaleSlope', 1),
        intercept=scan.metadata.get('RescaleIntercept', 0),
        windowCenter=window[0],
        windowWidth=window[1],
        slices=slices,
        rows=shape[1],
        columns=shape[2],
        color=scan.is_color_image(),
        pixelSpacing=scan.metadata.get('PixelSpacing', None),
        sliceThickness=scan.metadata.get('SliceThickness', None),
        frameOfReferenceUID=scan.metadata.get('FrameOfReferenceUID', None),
        imageOrientation=scan.image_orientation,
        imagePositions=scan.image_positions
    )

@data_urls.route('/scan/<uid>/<int:slice_number>/volume')
def get_slice_volume(uid, slice_number):
    #TODO create a local cache
    logging.info("Started at: {}".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
    try:
        scan = Scan.fromID(uid, app.config['CT_SCANS_DIR'],
                           prefer_compressed_volume=False,
                           compressed_volumes_dir=app.config['COMPRESSED_VOLUMES_DIR'])
        logging.info("Got scan: {}".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))

        volume = scan.volume
        slice_volume = volume[slice_number - 1]
        slice_volume = slice_volume.tobytes()
        logging.info("Got volume: {}".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))

        headers = Headers()
        headers['Content-Length'] = len(slice_volume)
        rv = app.response_class(slice_volume, mimetype='application/octet-stream', headers=headers)
        logging.info("Return at: {}".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
        return rv
    except IOError:
        app.logger.warning('Cannot find scan with id %s', uid)
        abort(404)
    pass
