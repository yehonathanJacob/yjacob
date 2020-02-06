var videoElement = document.querySelector('video');
var videoSelect = document.querySelector('#videoSource');
var buttonGo = document.getElementById('start_barcode');

navigator.mediaDevices.enumerateDevices()
.then(gotDevices).catch(handleError);

function gotDevices(deviceInfos) {
  var first = null;
  for (var i = 0; i <deviceInfos.length; i++) {
    var deviceInfo = deviceInfos[i];
    if (deviceInfo.kind === 'videoinput') {
      var label = document.createElement('label');
      label.classList.add("btn");
      label.classList.add("btn-secondary");
      label.setAttribute("for", "camera" + i);
      var input = document.createElement('input');
      input.setAttribute("type", "radio");
      input.setAttribute("name", "videoOptions");
      input.setAttribute("id", "camera" + i);
      input.setAttribute("value", deviceInfo.deviceId);
      if (videoSelect.childElementCount == 0)
        first = input;
      label.innerText = deviceInfo.label;
      label.appendChild(input);
      videoSelect.appendChild(label);
    }
  }
  $('input[type="radio"][name="videoOptions"]').on('click change',function(e){getStream(e.currentTarget);});
  if (first != null)
    getStream(first);
  else
    alert("There is no camera");
}

function getStream(radio) {
  if (window.stream) {
    window.stream.getTracks().forEach(function(track) {
      track.stop();
    });
  }
  var constraints = {
    video: {
      deviceId: {exact: radio.value}
    }
  };
  navigator.mediaDevices.getUserMedia(constraints).
    then(gotStream).catch(handleError);
}
function gotStream(stream) {
  window.stream = stream; // make stream available to console
  videoElement.srcObject = stream;
}

function handleError(error) {
  console.log('Error: ', error);
}

function check(){
  flag = true;
  if (videoElement.srcObject == null){
    flag = false;
    alert("please selecet a camera and dispaly it");
  }
  if (!window.ZXing){
    flag = false;
    alert("the process is not ready, try to realod the page");
  }
  return flag
}
function go(){
  buttonGo.disabled = true;
  scanBarcode(videoElement);
  document.getElementById("txtResult").innerText = data['textContent'];
  document.getElementById("otherResult").innerText = "is int: "+isNormalInteger(data['textContent']);
  buttonGo.disabled = false;
}

function isNormalInteger(str) {
    var n = Math.floor(Number(str));
    return n !== Infinity && String(n) === str && n >= 0;
}

//############### API #############
// prepare the ZXing
var ZXing = null;
var decodePtr = null;
var tick = function () {
  if (window.ZXing) {
    ZXing = ZXing();
    decodePtr = ZXing.Runtime.addFunction(decodeCallback);
  } else {
    setTimeout(tick, 10);
  }
};
tick();

//where data is saved
var data = {};

//process of each frame
var decodeCallback = function (ptr, len, resultIndex, resultCount) {
  data['result'] = new Uint8Array(ZXing.HEAPU8.buffer, ptr, len);
  data['textContent'] = String.fromCharCode.apply(null, data['result']);
  console.log(data['textContent']);
};

// scan barcode
function scanBarcode(videoElement) {

  if (ZXing == null) {
    alert("Barcode Reader is not ready!");
    return;
  }

  var vid = videoElement;
  console.log("video width: " + vid.videoWidth + ", height: " + vid.videoHeight);
  var barcodeCanvas = document.createElement("canvas");
  barcodeCanvas.width = vid.videoWidth;
  barcodeCanvas.height = vid.videoHeight;
  var barcodeContext = barcodeCanvas.getContext('2d');
  var imageWidth = vid.videoWidth, imageHeight = vid.videoHeight;
  barcodeContext.drawImage(videoElement, 0, 0, imageWidth, imageHeight);
  // read barcode
  var imageData = barcodeContext.getImageData(0, 0, imageWidth, imageHeight);
  var idd = imageData.data;
  var image = ZXing._resize(imageWidth, imageHeight);
  console.time("decode barcode");
  //copy video frame to the ZXing
  for (var i = 0, j = 0; i < idd.length; i += 4, j++) {
    ZXing.HEAPU8[image + j] = idd[i];
  }
  var err = ZXing._decode_any(decodePtr);//send the frame to ZXing process
  console.timeEnd('decode barcode');
  console.log("error code", err);
  if (err == -2) {
    setTimeout(scanBarcode(videoElement), 30);
  }
}