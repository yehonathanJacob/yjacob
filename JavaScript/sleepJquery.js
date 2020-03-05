
function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 1; i > 0; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}
