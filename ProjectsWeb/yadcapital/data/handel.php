<?php
// Handling data in JSON format on the server-side using PHP
//


// echo $_POST['To'].'dasdasd';
// // header("Content-Type: application/json");
// // // build a PHP variable from JSON sent using POST method
// // // $v = json_decode(stripslashes(file_get_contents("php://input")));
// // // build a PHP variable from JSON sent using GET method
// // $v = json_decode(stripslashes($_POST["data"]));
// // // encode the PHP variable to JSON and send it back on client-side
// // echo json_encode($v)."GET";


function end_seccion($status){
    $response = array();
	$response['posts'] = $status;
	$v = json_encode($response);
	echo $v;
	die();
}

header("Content-Type: application/json");
// build a PHP variable from JSON sent using POST method
$jsonText = file_get_contents("php://input");
$jsonData = json_decode(str_replace("<br>",'\n',$jsonText), true);

if (!isset($jsonData['oldPs']) 
	|| !isset($jsonData['oldUs']) 
	|| !isset($jsonData['actionOn'])){
	end_seccion("error in line 16".$jsonData['oldUs'].$jsonData['oldPs'].$jsonData['actionOn'].'l');
}

$fileName = 'datafile.json';
$contents = file_get_contents('../data/'.$fileName);
$oldData = json_decode($contents, true);
if ($jsonData['oldPs'][0] != $oldData['password'][0] or $jsonData['oldUs'][0] != $oldData['username'][0]){
 	end_seccion("error in line 23<br>".$jsonData['oldPs'][0].$oldData['password'][0].$jsonData['oldUs'][0].$oldData['username'][0]."");
}

$actionOn = $jsonData['actionOn'];

unset($jsonData['actionOn']);
unset($jsonData['oldPs']);
unset($jsonData['oldUs']);

$fp = fopen('../data/'.$fileName, 'w');
fwrite($fp, json_encode($jsonData));
fclose($fp);

if ($actionOn == "json")
{
	end_seccion('Data was saved on server!');
}

?>