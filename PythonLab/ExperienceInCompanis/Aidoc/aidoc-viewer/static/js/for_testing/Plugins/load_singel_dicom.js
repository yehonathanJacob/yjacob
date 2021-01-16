(function() {
    'use strict';

    function LoadSingelSlice(){
        EventEmitter2.call(this, { wildcard: true, delimiter: ':' });
        this.reset();
    }

    LoadSingelSlice.prototype = Object.create(EventEmitter2.prototype);

    LoadSingelSlice.prototype.reset = function (){
        this.scansBySeriesUID = {};
        this.studiesMetaData = {};
        this.selectedSeriesUID = null;
    };

    LoadSingelSlice.prototype.load_DICOM = function(workItem, seriesKey, sliceNumber) {
        aidocViewer.services.TimerServise.start_and_hide();
        var that = this;
        Promise.resolve(that.downloadStudyMetaData(workItem)).then(function () {
            var studyMetaData = that.studiesMetaData[workItem];

            if (!(that.test_series_key_is_number(seriesKey))) {
                seriesKey = Object.keys(studyMetaData['series'])[0];
            }

            var seriesUid = studyMetaData["series"][seriesKey].uid;
            if (that.selectedSeriesUID !== seriesUid){
                resetPage();
                that.selectedSeriesUID = seriesUid
            }

            Promise.resolve(that.downloadSliceVolume(workItem, seriesKey, sliceNumber)).then(function (resolve) {
                loadImageBasic(workItem, seriesUid, sliceNumber);
            });
        });
    };

    LoadSingelSlice.prototype.test_series_key_is_number = function (seriesKey){
        return /^\+?(0|[1-9]\d*)$/.test(seriesKey);
    };

    LoadSingelSlice.prototype.downloadStudyMetaData = function(workItem) {
        var that = this;
        if (workItem in that.studiesMetaData)
            return true;
        else {
            return Promise.resolve($.getJSON('data/study/' + workItem)).then(function (MetaData) {
                that.studiesMetaData[workItem] = MetaData;
            });
        }
    };

    LoadSingelSlice.prototype.downloadSliceVolume = function(workItem, seriesKey, sliceNumber) {
        var that = this;
        var studyMetaData = that.studiesMetaData[workItem];
        var seriesUid = studyMetaData["series"][seriesKey].uid;
        if (seriesUid in that.scansBySeriesUID && that.scansBySeriesUID[seriesUid].volume[sliceNumber - 1] != null) {
            return true;
        } else {
            var seriesMetaData = studyMetaData["series"][seriesKey];
            if (!(seriesUid in that.scansBySeriesUID))
            {
                var scanData = $.extend({}, seriesMetaData);
                scanData.volume = [];
                for (var i = 0; i < scanData.slices; i++) {
                    scanData.volume.push(null);
                }
                that.scansBySeriesUID[seriesUid] = scanData;
            }

            var xhr = $.ajax({
                url: 'data/scan/' + seriesUid + '/' + sliceNumber +'/volume',
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
                    var scanData = that.scansBySeriesUID[seriesUid];
                    if (!data.fromCache) {
                        var sliceVolumeBuffer = new Int16Array(data.volume);
                        scanData.volume[sliceNumber -1] = sliceVolumeBuffer;

                        var btnArr = [];
                        btnArr.push(that.prepareForHtmlBtnData(workItem, seriesKey, sliceNumber -1));

                        loadButtonToDicom(btnArr);
                    } else {
                        scanData.volume[sliceNumber -1] = data.volume;
                    }

                    that.scansBySeriesUID[seriesUid] = scanData;
                    return true;
                });
        }
    };

    LoadSingelSlice.prototype.prepareForHtmlBtnData = function (workItem,seriesKey,i){
      var btnData = {};
      var btn_num = i+1;
      btnData['onclick'] = "aidocViewer.plugins.LoadSingelSlice.load_DICOM('"+workItem+"', '"+seriesKey+"', "+btn_num+")";
      btnData['innerText'] = btn_num;
      return btnData;
    };

     aidocViewer.plugins.LoadSingelSlice = new LoadSingelSlice();
}());