<?php
if(isset($_POST['nul'])&&isset($_POST['upid'])&&isset($_POST['upty'])&&isset($_POST['upps'])&&isset($_POST['upde'])){
	$arr = explode('|',$_POST['nul']);
	$conn = new mysqli("sql145.main-hosting.eu.", "u976997437_sm", "WfkNBBNMrbp4", "u976997437_msqlp");
	if ($conn->connect_error) {
		$conn->close();
		die("Connection failed: " . $conn->connect_error);}
	$user = $conn->real_escape_string(htmlentities($arr[0]));
	$ps = $conn->real_escape_string(htmlentities($arr[1]));
	$upid = $conn->real_escape_string(htmlentities($_POST['upid']));
	$upty = $conn->real_escape_string(htmlentities($_POST['upty']));
	$upps = $conn->real_escape_string(htmlentities($_POST['upps']));
	$upde = $conn->real_escape_string(htmlentities($_POST['upde']));
	$check="False";
	$result = $conn->query('SELECT * FROM MyUsers');
	while($object = $result->fetch_object()){
		if((strtolower($user)==strtolower($object->UserName))&&(strtolower($ps)==strtolower($object->Password))){
				$check="True";
				break;
		}		
	}	
	if($check == "True"){
		$sql ='UPDATE '.strtolower($user).' SET Type="'.$upty.'",Password="'.$upps.'",Details="'.$upde.'" WHERE id='.$upid.'';
		if ($conn->query($sql) === TRUE) {
			die("True");
		} else {
			die($sql . "\n" . $conn->error);
		}	
	}else{die("Didn't find the right User");}
}else{
	die("Didn't got the right DATA");
}
?>