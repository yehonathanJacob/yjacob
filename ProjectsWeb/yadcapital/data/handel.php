<?php
// Handling data in JSON format on the server-side using PHP
//

function end_seccion($status){
    $response = array();
	$response['posts'] = $status;
	$v = json_encode($response);
	echo $v;
	die();
}
function render_php($path,array $args){
    ob_start();
    include($path);
    $var=ob_get_contents(); 
    ob_end_clean();
    return $var;
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

if ($actionOn == "test" || $actionOn == "production"){
	if ($actionOn == "test"){
		$args = array('URL' => 'http://test.yadcapital.com', 'directory' => '../test/files/');
	}
	if ($actionOn == "production"){
		$args = array('URL' => 'https://yadcapital.com', 'directory' => '../files/');
	}
	$fileIndexName = 'index.html';

	$HTML_PAGE = render_php('render.php', $args);

	$fHtml = fopen($args['directory'].$fileIndexName, 'w');
	fwrite($fHtml, $HTML_PAGE);
	fclose($fHtml);

	end_seccion($actionOn.' was update. The uploaded data was save also.');	
}

end_seccion('Action was not found.');
?>