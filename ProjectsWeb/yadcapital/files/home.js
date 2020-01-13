function ScrollTo(buttonObj){
  var name = buttonObj.getAttribute('id');
  name = name.replace("Button","");
  (name != "home") ?  $('html, body').stop().animate({ scrollTop: $("."+name+" .Ftitle").offset().top - $("nav").height() -20}, 900) : $('html, body').stop().animate({ scrollTop: 0}, 900);  
  document.getElementById("menueButton").classList.toggle("show");
  document.getElementById("menueContainer").classList.toggle("show");
}
var userAgent = window.navigator.userAgent;
$(document).ready(function(){
	resize();	
});
$(window).resize(function(){
resize();
});
function resize() {
	winHeight = window.innerHeight - $("nav").height();	
	if (userAgent.match(/iPad/i) || userAgent.match(/iPhone/i)) {
	   	$("header").css("min-height",window.innerHeight+"px");
		$(".form").css("min-height",winHeight+"px");
		$("header, .form").addClass("backgroundFix");
	}
}
$(window).scroll(function(){	
  if( $(window).scrollTop() >= winHeight ){
    $("nav").addClass('scroll');
	}
	else{
		$("nav").removeClass('scroll');
	}	
});
/*AOS OnScroll (JS)*/
AOS.init({
  duration: 1200,
});
/*parallax-window*/
$('.walkingPeople').parallax({imageSrc: 'images/walkingPeople.jpg'});
function navigationOC(x) {
	x.classList.toggle("show");
	document.getElementById("menueContainer").classList.toggle("show");
}
function sendMail(){
	var conatactToSend = "daniel@yadcapital.com, david@yadcapital.com";
	var textMessage = "" +
			"Name: "+document.getElementsByName("name")[0].value +
			"\nSubject: "+document.getElementsByName("subject")[0].value +
			"\nE-mail: "+document.getElementsByName("email")[0].value +
			"\nTelephone: "+document.getElementsByName("tel")[0].value +
			"\nMessage: "+document.getElementsByName("message")[0].value;
	if(confirm("This Message will be sent:\n"+textMessage+"\nTo: "+conatactToSend))
		{
			var xhttp;
			if (window.XMLHttpRequest) {
			// code for modern browsers
			xhttp = new XMLHttpRequest();
			} else {
			// code for old IE browsers
			xhttp = new ActiveXObject("Microsoft.XMLHTTP");
			}			
			xhttp.onreadystatechange = function() {
				if (this.readyState == 4) {
					if(this.status == 200)
						alert(this.responseText);
					else
						alert("Error.\nError code: "+this.status+"\nResponse Text: "+ this.responseText);
				}
			};
			xhttp.open("POST", "https://yadcapital.com/files/sendMail.php", true);
			xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
			xhttp.send("To="+conatactToSend+"&Message="+textMessage+"&Subject=New E-Mail from a Client");
		}
}