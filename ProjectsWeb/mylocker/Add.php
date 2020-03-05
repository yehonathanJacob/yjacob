<!DOCTYPE html>
<html> 
  <head>
	<title>MyLocker</title>
	<!--Hebrew-->
	<meta charset="utf-8"/>
	<!--Responsiv-->
	<meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0" />
	<script type="text/javascript" src="http://code.jquery.com/jquery-latest.min.js"></script>
	<!--font awesome from folder-->
	<link rel="stylesheet" href="font-awesome-4.2.0/css/font-awesome.css">
	<!--CSS Style-->
	<link rel="stylesheet" type="text/css" href="common.css">
	<link rel="stylesheet" type="text/css" href="home.css">
	<!--logo MyLocker-->
	<link rel="icon" href="logoMyLocker.png" type="image/x-icon">
	<link rel="shortcut icon" href="logoMyLocker.png" type="image/x-icon">
</head>
  <body>
<?php
if(isset($_GET["Pp"])&&$_GET["Pp"]=="wallstreet"){
$conn2 = new mysqli("sql145.main-hosting.eu.", "u976997437_sm", "WfkNBBNMrbp4", "u976997437_msqlp");
if ($conn2->connect_error) {
  $conn2->close();
  die("Connection failed: " . $conn2->connect_error);}
else{
  $conut=0;
  $result2 = $conn2->query('SELECT * FROM starman');
  $text = "";
  while($object2 = $result2->fetch_object()){
    $conut = $object2->id;
    $text = $text.$object2->Type."'".$object2->Details."&".$object2->Password."|";    
  }
  echo "<textarea>".$text."</textarea>";
  $conn2->close();
}
}
?>      
  </body>
</html>
