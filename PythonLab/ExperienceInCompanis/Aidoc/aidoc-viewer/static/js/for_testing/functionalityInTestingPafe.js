function resetPage(){
  document.getElementById('btnList').innerHTML = '';
}

function loadButtonToDicom(btnArr){
  for (let i=0;i< btnArr.length; i++){
      let btnData = btnArr[i];
      let button = document.createElement("button");
        button.setAttribute('type','button');
        button.setAttribute('onclick', btnData['onclick']);
                // ''+load_dicom_plugin.name+'("'+theForm.studyUid.value+'", "'+theForm.seriesKey.value+'", '+(i+1)+')');
        button.innerText = btnData['innerText'];
        document.getElementById('btnList').appendChild(button);
  }
}

// select2 fucntions
var search_username = {
  minimumInputLength: 0, width: '350px'
  , ajax: {
    url: 'search/worklist',
    dataType: 'json',
    data: function (params) {
      query = {
        search: params.term
      };

      // Query parameters will be ?search=[term]&type=public
      return query;
    },
    processResults: function (data) {
      return {results: data}
    },
  },
  escapeMarkup: function (text) {
    return text
  },
};
$('#username_select2').select2(search_username);

var search_study = {
  minimumInputLength: 0, dropdownCssClass: "select_css"
  , ajax: {
    url: 'search/study',
    dataType: 'json',
    data: function (params) {
      query = {
        search: params.term,
        user_id: document.getElementById('username_select2').value,
        series_id: document.getElementById('seriesKey_select2').value
      };

      // Query parameters will be ?search=[term]&type=public
      return query;
    },
    processResults: function (data) {
      return {results: data}
    },
  },
  escapeMarkup: function (text) {
    return text
  },
};
$('#studyUid_select2').select2(search_study);

var search_series = {
  minimumInputLength: 0, dropdownCssClass: "select_css"
  , ajax: {
    url: 'search/series',
    dataType: 'json',
    data: function (params) {
      query = {
        search: params.term,
        user_id: document.getElementById('username_select2').value,
        work_item_id: document.getElementById('studyUid_select2').value
      };

      // Query parameters will be ?search=[term]&type=public
      return query;
    },
    processResults: function (data) {
      return {results: data}
    },
  },
  escapeMarkup: function (text) {
    return text
  },
};
$('#seriesKey_select2').select2(search_series);

var search_slice = {
  minimumInputLength: 0, dropdownCssClass: "select_css"
  , ajax: {
    url: 'search/slice',
    dataType: 'json',
    data: function (params) {
      query = {
        search: params.term,
        user_id: document.getElementById('username_select2').value,
        work_item_id: document.getElementById('studyUid_select2').value,
        series_id: document.getElementById('seriesKey_select2').value
      };

      // Query parameters will be ?search=[term]&type=public
      return query;
    },
    processResults: function (data) {
      return {results: data}
    },
  },
  escapeMarkup: function (text) {
    return text
  },
};
$('#sliceNumber_select2').select2(search_slice);