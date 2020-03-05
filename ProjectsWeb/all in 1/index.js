function ScrollTo(element,navheight){
  $('html, body').stop().animate({ scrollTop: $(element).offset().top - navheight-25}, 900);
}
function RGBA(e, alpha) { //e = jQuery element, alpha = background-opacity
    b = e.css('backgroundColor');
    e.css('backgroundColor', 'rgba' + b.slice(b.indexOf('('), ( (b.match(/,/g).length == 2) ? -1 : b.lastIndexOf(',') - b.length) ) + ', '+alpha+')');
		$("nav #navTitle").css('opacity',alpha);
}
var winHeight;var navHeight;var id;var bt;
$(window).load(function() {	
	resize();
});
$(window).resize(function(){
	resize();
});
function resize() {	
	winHeight = $("header").height();	
	navHeight = $("nav").height();	
	$("header #backImg img").css('height',winHeight);
	$("header #back").css('height',winHeight);
	if($(window).width()>768){
		$("nav #navBar").css("display","block");
		$("#form2 #buttonContainer .button .btText").css("display","none");
	}
	else{
		$("nav #navBar").css("display","none");
		$("#form2 #buttonContainer .button .btText").css("display","inline-block");
	}
}
$("nav #navBarBtn").click(function(){
	if($("nav #navBar").css('display') == 'none')
	{
		navHeight = $("nav").height()-5;
		$("nav #navBar").slideDown(800);		
	}else{
		$("nav #navBar").slideUp(800);
	}
});
$("#goDown").click(function(){
	$("html body").stop().animate({ scrollTop: $("header").height() - $("nav").height()}, 900);
});
var Ops;var nav=$("nav");
$(window).scroll(function(){
	Ops = $(window).scrollTop()/(winHeight-navHeight);
	RGBA(nav,Ops);
});
$('nav #LanBtn').hover(function() {
  if($("header").width()>768){$('nav #LanBtn #i').show(300);}
  }, function() {    
    $('nav #LanBtn #i').hide(300);
  });
$("nav .navBt").click(function(){
	if($(window).width()<769){
		$("nav #navBar").slideUp(800);		
	}
	id = $(this).attr("id");
	id = id.replace("f","");
	id = "form"+id;
	ScrollTo($("#"+id),navHeight+12);	
});
$("#form2 #buttonContainer .button").mousemove(function(){
	if($("header").width()>768){
		bt = $(this).attr("id");
		$("#form2 #buttonContainer #"+bt+".button .btText").show(300);
		$(this).addClass("buttonPr");
	}
});
$("#form2 #buttonContainer .button").mouseleave(function(){
	if($("header").width()>768){
		bt = $(this).attr("id");
		$("#form2 #buttonContainer #"+bt+".button .btText").hide(300);
		$(this).removeClass("buttonPr");
	}
});
var fullName;var phoneNumber;var email;var topic;var details;
var messsage;
function sendMessage(){
	fullName = $('#form3 #ContactForm form input[name="fullName"]').val();	
	phoneNumber = $('#form3 #ContactForm form input[name="phoneNumber"]').val();
	email = $('#form3 #ContactForm form input[name="email"]').val();
	topic = $('#form3 #ContactForm form input[name="topic"]').val();
	details = $('#form3 #ContactForm form textarea').val();
	messsage = "Full Name: "+fullName+"\nPhone Number: "+phoneNumber+"\nEmail: "+email+"\nTopic of message: "+topic+"\nDetails of message: "+details;
	if(confirm("Do you want to send this message to the project manger?\n"+messsage)){
		$.post("Function.php",{
        Fun:"sendMessage",
			topic:topic,
        messsage:messsage        
      }, function(response){
			if(response == "True"){
				alert("The message was sent to as.\n we will contact you soon as posibel.");
				location.reload();
			}
			else
			{
				alert('Error:\n'+response);          
			}
			});
	}
}
var paymentId="";
var amount="";var firstName="";var lastName="";var address1;var address2;var city;var state;var night_phone_a="";var email;
function payById(){	
	paymentId = $('#form4 form input[name="paymentId"]').val();
	if(paymentId !== ""){
		$.post("Function.php",{
		Fun:"paymentById",
		id:$('#form4 form input[name="paymentId"]').val()
		}, function(response){
			if(response=="False"){alert("There is no such a payment");}
			else{
				var form = $(response);
				$('body').append(form);
				form.submit();
			}
		});
	}else{
		alert("Please enter your payment ID");
	}
}
function payByForm(){	
	amount = $('#form4 form input[name="amount"]').val();
	firstName = $('#form4 form input[name="firstName"]').val();
	lastName = $('#form4 form input[name="lastName"]').val();
	night_phone_a = $('#form4 form input[name="night_phone_a"]').val();
	if(amount !== ""&&firstName !== ""&&lastName !== ""&&night_phone_a !== ""){
		address1 = $('#form4 form input[name="address1"]').val();
		address2 = $('#form4 form input[name="address2"]').val();
		city = $('#form4 form input[name="city"]').val();
		state = $('#form4 form input[name="state"]').val();
		email = $('#form4 form input[name="email"]').val();		
		$.post("Function.php",{
		Fun:"paymentByForm",
		firstName:firstName,
		lastName:lastName,
		night_phone_a:night_phone_a,
		address1:address1,
		address2:address2,
		city:city,
		state:state,
		email:email,
		amount:amount	
		}, function(response){			
			if(response.indexOf("False")==0){alert("There Wass an Error: "+response);}
			else{
				var form = $(response);
				$('body').append(form);
				form.submit();
			}
		});
	}else{
		alert("Please enter the amount, first name, last name an your phone number");
	}
}