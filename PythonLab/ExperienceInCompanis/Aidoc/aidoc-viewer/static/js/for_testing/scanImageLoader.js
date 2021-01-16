(function() {
    'use strict';

    function scanImageLoader(imageId) {
        var deferred = $.Deferred();
        // var imageInfo = aidocViewer.utils.imageIdUtils.split(imageId);
        var imageInfo = splitImageId(imageId);
        var workItem = imageInfo.workItem;
        var seriesUID = imageInfo.seriesUID;
        var sliceNum = imageInfo.sliceNum;

        var scan = load_dicom_plugin.scansBySeriesUID[seriesUID];
        var study = load_dicom_plugin.studiesMetaData[workItem];
        // var study = aidocViewer.services.ScanService.study;
        // var scan = aidocViewer.services.ScanService.scans[uid];

        aidocViewer.services.TimerServise.stop_and_display();


        if (sliceNum <= scan.slices) {
            var minmax = getMinMaxPixelValues(scan.volume[sliceNum - 1]);
            var pixelSpacing = getPixelSpacing();

            var image = {
                imageId: imageId,
                minPixelValue: minmax.min,
                maxPixelValue: minmax.max,
                slope: scan.slope,
                intercept: scan.intercept,
                windowCenter: scan.windowCenter,
                windowWidth: scan.windowWidth,
                getPixelData: getPixelData,
                rows: scan.rows,
                columns: scan.columns,
                height: scan.rows,
                width: scan.columns,
                color: scan.color,
                columnPixelSpacing: pixelSpacing.column,
                rowPixelSpacing: pixelSpacing.row,
                invert: false,
                sizeInBytes: scan.rows * scan.columns * 2
            };
            return deferred.resolve(image);
        } else {
            return deferred.reject({error: 'Invalid slice: ' + sliceNum});
        }

        function getPixelData() {
            return scan.volume[sliceNum - 1];
        }

        function getMinMaxPixelValues(pixelData) {
            // we always calculate the min max values since they are not always
            // present in DICOM and we don't want to trust them anyway as cornerstone
            // depends on us providing reliable values for these
            var min = 65535;
            var max = -32768;
            var numPixels = pixelData.length;

            for (var index = 0; index < numPixels; index++) {
                var spv = pixelData[index];
                min = Math.min(min, spv);
                max = Math.max(max, spv);
            }

            return {
                min: Math.min(min, 0),
                max: Math.max(max, 5024)
            };
        }

        function getPixelSpacing() {
            var pixelSpacing = {
                column: 1.0,
                row: 1.0
            };

            if (scan.pixelSpacing && scan.pixelSpacing.length > 0) {
                pixelSpacing.row = scan.pixelSpacing[0];

                if (scan.pixelSpacing.length > 1) {
                    pixelSpacing.column = scan.pixelSpacing[1];
                }
            }
            return pixelSpacing;
        }
    }

    cornerstone.registerImageLoader('aidoc', scanImageLoader);
}());