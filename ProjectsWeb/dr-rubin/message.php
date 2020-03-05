<?php
if(!isset($_POST["g-recaptcha-response"])){die("Hello Bots");}
$url = 'https://www.google.com/recaptcha/api/siteverify';
$data = array('secret' => '6LdTOBgUAAAAAEPfWQv1UMOUiiPlFLBVzBsJQ74V', 'response' => $_POST["g-recaptcha-response"]);

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
$json = json_decode($result, true);
if(!$json['success']){die("You Didn't Clike on 'I am not a robot");} 

if(isset($_POST['fullName'])&&isset($_POST['topic'])&&isset($_POST['tel'])&&isset($_POST['email'])&&isset($_POST['details']))
{
  $message = "Full Name: ".htmlentities($_POST['fullName'], ENT_QUOTES , "UTF-8")."\nTopic: ".htmlentities($_POST['topic'], ENT_QUOTES , "UTF-8")."\nTell: ".htmlentities($_POST['tel'], ENT_QUOTES , "UTF-8")."\nE-Mail: ".htmlentities($_POST['email'], ENT_QUOTES , "UTF-8")."\nDetails: \n".htmlentities($_POST['details'], ENT_QUOTES , "UTF-8");
  if(mail("yld.rubin@gmail.com","Mail From a Client",$message)){die("<h2>Your message has been sent</h2><br><a href='/'>Clike To Go Back</a>");}
  else{die("Error in sending message");}  
}else{die("Error In Data");}
?>