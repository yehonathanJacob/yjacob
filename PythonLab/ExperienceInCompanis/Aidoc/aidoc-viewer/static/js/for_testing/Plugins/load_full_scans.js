(function() {
    'use strict';

    function LoadFullScans(){
        EventEmitter2.call(this, { wildcard: true, delimiter: ':' });
        this.reset();
    }

    LoadFullScans.prototype = Object.create(EventEmitter2.prototype);

    LoadFullScans.prototype.reset = function (){
        this.scansBySeriesUID = {};
        this.studiesMetaData = {};
    };

    LoadFullScans.prototype.load_DICOM = function(workItem, seriesKey, sliceNumber) {
        aidocViewer.services.TimerServise.start_and_hide();
        var that = this;
        Promise.resolve(that.downloadStudyMetaData(workItem)).then(function () {
            var studyMetaData = that.studiesMetaData[workItem];

            if (!(that.test_series_key_is_number(seriesKey))) {
                seriesKey = Object.keys(studyMetaData['series'])[0];
            }

            Promise.resolve(that.downloadSeriesVolume(workItem, seriesKey)).then(function (seriesUid) {
                loadImageBasic(workItem, seriesUid, sliceNumber);
            });
        });
    };

    LoadFullScans.prototype.test_series_key_is_number = function (seriesKey){
        return /^\+?(0|[1-9]\d*)$/.test(seriesKey);
    };

    LoadFullScans.prototype.downloadStudyMetaData = function(workItem) {
        var that = this;
        if (workItem in that.studiesMetaData)
            return true;
        else {
            return Promise.resolve($.getJSON('data/study/' + workItem)).then(function (MetaData) {
                that.studiesMetaData[workItem] = MetaData;
            });
        }
    };

    LoadFullScans.prototype.downloadSeriesVolume = function(workItem, seriesKey) {
        var that = this;
        var studyMetaData = that.studiesMetaData[workItem];
        var seriesUid = studyMetaData["series"][seriesKey].uid;
        if (seriesUid in that.scansBySeriesUID) {
            return seriesUid;
        } else {
            var seriesMetaData = studyMetaData["series"][seriesKey];
            var xhr = $.ajax({
                url: 'data/scan/' + seriesUid + '/volume',
                type: 'GET',
                dataType: 'binary',
                processData: false,
                responseType: 'arraybuffer',
            });

            return Promise.resolve(xhr)
                .then(function (results) {
                    console.log("success");
                    return {fromCache: false, volume: results};
                })
                .catch(function (e) {
                    console.log("error");
                    throw e;
                }).then(function (data) {
                    var scanData = $.extend({}, seriesMetaData);
                    if (!data.fromCache) {
                        var scanVolumeBuffer = new Int16Array(data.volume);
                        scanData.volume = [];

                        var sliceSize = scanData.rows * scanData.columns;
                        var btnArr = [];
                        for (var i = 0; i < scanData.slices; i++) {
                            scanData.volume.push(scanVolumeBuffer.subarray(i * sliceSize, (i * sliceSize) + sliceSize));
                            btnArr.push(that.prepareForHtmlBtnData(workItem, seriesKey, i));
                        }
                        resetPage();
                        loadButtonToDicom(btnArr);
                    } else {
                        scanData.volume = data.volume;
                    }

                    that.scansBySeriesUID[seriesUid] = scanData;

                    return seriesUid;
                });
        }
    };

    LoadFullScans.prototype.prepareForHtmlBtnData = function (workItem,seriesKey,i){
      var btnData = {};
      var btn_num = i+1;
      btnData['onclick'] = "aidocViewer.plugins.LoadFullScans.load_DICOM('"+workItem+"', '"+seriesKey+"', "+btn_num+")";
      btnData['innerText'] = btn_num;
      return btnData;
    };

     aidocViewer.plugins.LoadFullScans = new LoadFullScans();
}());