import logging
from concurrent.futures import ThreadPoolExecutor

from scan import Scan


logger = logging.getLogger(__name__)


def compress_scan_volume(ct_scans_dir, compressed_volumes_dir, uid, overwrite=False):
    try:
        scan = Scan.fromID(uid, scanfolder=ct_scans_dir, compressed_volumes_dir=compressed_volumes_dir)
        if overwrite or (not scan.volume_compressed):
            logger.info('Compressing scan volume for uid %s', uid)
            scan.store_compressed_volume()
            logger.info('Scan volume compression for uid %s completed successfully', uid)
    except Exception as e:
        logger.exception('Cannot compress scan volume for uid %s', uid)


class ScanCompressor:
    def __init__(self, ct_scans_dir, compressed_volumes_dir=None):
        self.ct_scans_dir = ct_scans_dir
        self.compressed_volumes_dir = compressed_volumes_dir or ct_scans_dir
        self.executor = ThreadPoolExecutor(max_workers=1)

    def compress(self, uid, overwrite=False):
        self.executor.submit(compress_scan_volume, self.ct_scans_dir, self.compressed_volumes_dir, uid, overwrite)

    def destroy(self):
        self.executor.shutdown()
