var SendMessagesHight,HeaderHight;
$( window ).resize(reset_OutputMessages_bottom);
function reset_OutputMessages_bottom() {
    SendMessagesHight = $("form")[0].offsetHeight;
    HeaderHight = $("header")[0].offsetHeight;
    $("#OutputMessages").css("margin-bottom",SendMessagesHight);
    $("#OutputMessages").css("margin-top",HeaderHight);
}
$( document ).ready(function() {
    reset_OutputMessages_bottom();
});
/*AOS OnScroll (JS)*/
AOS.init({
  duration: 100,
});