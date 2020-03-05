<?php
if(isset($_POST['User'])&&isset($_POST['Ps']))
{
	$conn = new mysqli("sql145.main-hosting.eu.", "u976997437_sm", "WfkNBBNMrbp4", "u976997437_msqlp");
	if ($conn->connect_error) {
		$conn->close();
		die("Connection failed: " . $conn->connect_error);}
	$user = $conn->real_escape_string(htmlentities($_POST['User']));
	$ps = $conn->real_escape_string(htmlentities($_POST['Ps']));

	$result = $conn->query('SELECT * FROM MyUsers');
	while($object = $result->fetch_object()){
		if((strtolower($user)==strtolower($object->UserName))&&($ps==$object->Password))
			{$conn->close();
			die("True");}
	}
	$conn->close();
	die("Wrong user name or password");
}
else{
	die('Erorr in getting info');
}
?>