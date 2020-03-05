function ScrollTo(element,navheight){
  $('html, body').stop().animate({ scrollTop: $(element).offset().top - navheight-15}, 900);
}
var winHeight;
$(window).resize(function(){
resize();
});
function resize() {
	winHeight = $("header").height() - $("nav").height();
	var lanHeight = $("nav #lan").height();
	$("nav").css('min-height',15+lanHeight);	
}
$(window).scroll(function(){	
  if( $(window).scrollTop() >= winHeight ){
    $("nav").addClass('addBackground');
	}
	else{
		$("nav").removeClass('addBackground');
	}
	if($(window).scrollTop() >= 20)
	{
		$("body").removeClass('activeScrool');
	}else{$("body").addClass('activeScrool');}
});
$("#goDownButton").click(function(){
	$("html, body").stop().animate({ scrollTop: winHeight}, 900);
});
//link click
var open = $('#home');
$("nav #barlink a").click(function(){
	ScrollTo($('#' + $(this).attr("class").toLowerCase()),$("nav").height());
	//$('#' + $(this).text().toLowerCase()).slideDown(300);		
});
//moreLan
var uk= $('#moreLan');
$('#lan').click(function(){
   if(uk.css('display') == 'block')
   {      
      uk.slideUp(300);
   }
   else{      
      uk.slideDown(300);
   }
});
function SendMessage(){
	var response = grecaptcha.getResponse();
	if(response != ""){
		$("form").submit();
	}else{
		alert("please check the 'I am not a robot button'");
	}		
}
$(document).ready(function(){
resize();
if ($( "#spesialLink" ).length && $("p strong[title='"+$( "#spesialLink" ).attr('name')+"']").length) 
{	
	$("p strong[title='"+$( "#spesialLink" ).attr('name')+"']").addClass("mark");
	ScrollTo($("#about p strong"),$('nav').height());	
	$("nav").addClass('addBackground');
}
});