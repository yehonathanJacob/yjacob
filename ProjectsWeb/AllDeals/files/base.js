var navS = document.getElementsByTagName("nav")[0];
var navButtonCointainer = document.getElementById("buttonContainer");
function openBar() {
    navS.classList.toggle("showMenue");
}
$("#navigationContainer").click(function(){
	navS.classList.remove("showMenue");
});
function resize(){
	if(window.innerWidth>768){
		navButtonCointainer.className = "btn-group btn-group-lg";
	}
	else{
		if(window.innerWidth>570)
		{
			navButtonCointainer.className = "btn-group btn-group-md";
		}
		else{
			navButtonCointainer.className = "btn-group-vertical btn-group-lg";
		}
	}
}
$(document).ready(function()
{	
	if( /Android|webOS|iPhone|iPad|iPod|Opera Mini/i.test(navigator.userAgent) ) {
		 document.getElementsByTagName("body")[0].classList.remove("desctop");
	}
	resize();
	$('#btn_Form4').click(function(e){
    	e.stopPropagation();
    	$("#enable-toolbar-trigger").trigger("click");
    	$('#btn_Form4').focusout();
	});
});