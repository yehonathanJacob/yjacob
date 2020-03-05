<!DOCTYPE html>
<html>
<head>
	<title></title>
	<!--Google reCAPTCHA-->
	<script src='https://www.google.com/recaptcha/api.js'></script>	
	<!--This Script to create and roll all tho rechaptcha button-->
	<script type="text/javascript">	
		var GoogleCheck1;var GoogleCheck2;
		var onloadCallback = function() {//this is the name of the function the create the button
		GoogleCheck1 = grecaptcha.render('GoogleCheck1', {//the id of the button
		'sitekey' : '6LdTOBgUAAAAABnQOnadEQ_dODCP6KrQfhi2FGxv',//hear you set up your private key
		'size' : 'compact' //size compact
		});
		GoogleCheck2 = grecaptcha.render('GoogleCheck2', {//the id of the button
		'sitekey' : '6LdTOBgUAAAAABnQOnadEQ_dODCP6KrQfhi2FGxv',//hear you set up your private key	  
		});
		};
		$(window).load(function(){
			 onloadCallback();
		});
		//you can use grecaptcha.getResponse(GoogleCheck1); To Check the fist button
		//if(grecaptcha.getResponse(GoogleCheck1) !== ""){ button is checked...}
	</script>
</head>
<body>
<form method="post" action="goToPHP.php">
<!--id will be the name of the buttton-->
<div class="googleCheckBt" id="GoogleCheck1"></div>
</form>
<!--Google reCAPTCHA-->
<script src="https://www.google.com/recaptcha/api.js?onload=onloadCallback&render=explicit" async defer></script>
</body>
</html>

<!--goToPHP.php-->
<?php
if(!isset($_POST["g-recaptcha-response"])){die("Hello Bots");}//if it is a robot it will stop hear.
$url = 'https://www.google.com/recaptcha/api/siteverify';
//Type in secret your secert Key
$data = array('secret' => '6LdTOBgUAAAAAEPfWQv1UMOUiiPlFLBVzBsJQ74V', 'response' => $_POST["g-recaptcha-response"]);//this is the post value arriver from the html page

// use key 'http' even if you send the request to https://...
$options = array(
    'http' => array(
        'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
        'method'  => 'POST',
        'content' => http_build_query($data)
    )
);

$context  = stream_context_create($options);
$result = file_get_contents($url, false, $context);
if ($result === FALSE) { die("Error In Google Recaptcha"); }
$json = json_decode($result, true);//json To Arry
if(!$json['success']){die("You Didn't Clike on 'I am not a robot");}//if he didn't clike, it will stop hear.
else{die("connected");}
?>
