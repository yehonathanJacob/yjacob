function loadImageBasic(workItem, seriesUid, sliceNumber){
    const element = document.querySelector('.cornerstone-element');
    // element.innerHTML = '';
    cornerstone.enable(element);
    const imageId = 'aidoc:'+workItem+'/'+seriesUid+'/'+sliceNumber;
    cornerstone.loadImage(imageId).then(function (image) {
      cornerstone.displayImage(element, image);
    });
}

function splitImageId(imageId) {
    // if (!isValidImageId(imageId)) {
    //     throw 'Invalid image id: ' + imageId;
    // }

    var parts = imageId.replace('aidoc:', '').split('/');
    var workItem = parts[0];
    var seriesUID = parts[1];
    var sliceNum = parseInt(parts[2]);
    return {
        workItem:workItem,
        seriesUID: seriesUID,
        sliceNum: sliceNum
    };
}