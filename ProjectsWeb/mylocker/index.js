function TryLog(elemnt){
if($(elemnt).attr("id")=="TryLog"){
if ($('#LogLoad').css('display') == 'none'){
	$('#LogLoad').slideToggle('medium', function() {    
        $(this).css('display','block');    });
}
var UserName = $('#LogUserName').val();
var Ps = $('#LogPassworrd').val();
if(grecaptcha.getResponse(GoogleCheck1) !=="" ){
if(UserName!=""&&Ps!="")
{
$.post("checkLog.php",{
        User:UserName,
        Ps:Ps,
    }, function(response){
    	if(response == "True")
    		$('#LogInPage').submit();
    	else
        {
    		alert('Please check your User Name and Password\n'+response);
            $('#LogLoad').slideUp(500);
        }
    });
}
else{
	alert("Please fill UserName and Password");
	$('#LogLoad').slideUp(500);
}}else{
	alert("Please clike on 'I am not a robot'");
	$('#LogLoad').slideUp(500);
}
}
}

function TrySign(elemnt){
if($(elemnt).attr("id")=="TrySign"){
if ($('#SignLoad').css('display') == 'none'){
	$('#SignLoad').slideToggle('medium', function() {    
        $(this).css('display','block');    });
}
var NewUserName = $('#NUser').val();
var NewPs = $('#NPassword').val();
var RPs = $(elemnt).parent().find('input[name="NRPassword"]').val();
var email= $(elemnt).parent().find('input[name="NMail"]').val();
var eror = "";
if(NewUserName.length<5||NewUserName.length>15)
eror+="* User Name is between 5 and 15 chars\n";
if(NewPs.length<5||NewPs.length>15)
eror+="* Password is between 5 and 15 chars\n";
if(NewPs!=RPs)
eror+="* Password and Re Password dosn't match\n";
if(email.indexOf('@')<0||email.length<10)
eror+="* Un real E-mail\n";
if(grecaptcha.getResponse(GoogleCheck2) === "" )
eror+="* Please clike on 'I am not a robot'\n";

if(eror!="")
{alert("Please check the next Error:\n"+eror);}
else{
	$.post("chekSign.php",{
        User:NewUserName,
        Ps:NewPs,
        Email:email
    }, function(response) {                 
        if(response != "")
        	alert(response);
        else{
        	alert("Your account has been created!");
        	$( "#LogUserName" ).val(NewUserName);
        	$( "#LogPassworrd" ).val(NewPs);
        	$('#LogInPage').submit();
        }
    });
}
$('#SignLoad').slideUp(500);
}
}

$('#TryLog').click(function () {
	TryLog($(this));
});

$('#TrySign').click(function(){
	TrySign($(this));
});
$(window).resize(function(){
    grecaptchaWidth = 304;
    formWidth = $("#LogInPage").width();
    scale = formWidth/grecaptchaWidth;
    if(scale < 1 ){
        $("#GoogleCheck1").css({"transform":"scale("+scale+")" , "margin-left" : "-"+((1-scale)*152)+"px"});
    }else{$("#GoogleCheck1").css({"transform":"scale(1)" , "margin-left" : "0"});}
});
