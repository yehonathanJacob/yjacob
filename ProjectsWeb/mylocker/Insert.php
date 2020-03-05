<?php
if(isset($_POST['nul'])&&isset($_POST['NewTy'])&&isset($_POST['NewPs'])&&isset($_POST['NewDetails'])){
	$arr = explode('|',$_POST['nul']);
	$conn = new mysqli("sql145.main-hosting.eu.", "u976997437_sm", "WfkNBBNMrbp4", "u976997437_msqlp");
	if ($conn->connect_error) {
		$conn->close();
		die("Connection failed: " . $conn->connect_error);}
	$user = $conn->real_escape_string(htmlentities($arr[0]));
	$ps = $conn->real_escape_string(htmlentities($arr[1]));
	$NewTy = $conn->real_escape_string(htmlentities($_POST['NewTy']));
	$NewPs = $conn->real_escape_string(htmlentities($_POST['NewPs']));
	$NewDetails = $conn->real_escape_string(htmlentities($_POST['NewDetails']));	
	$check="False";
	$result = $conn->query('SELECT * FROM MyUsers');
	while($object = $result->fetch_object()){
		if((strtolower($user)==strtolower($object->UserName))&&(strtolower($ps)==strtolower($object->Password))){
				$check="True";
				break;
		}		
	}	
	if($check == "True"){
		$sql ="INSERT INTO ".strtolower($user)." (Type, Password,Details)
				VALUES ('".$NewTy."', '".$NewPs."','".$NewDetails."')";
		if ($conn->query($sql) === TRUE) {
      $last_id = $conn->insert_id;
			die("True".$last_id);
		} else {
			die($sql . "\n" . $conn->error);
		}	
	}else{die("Didn't find the right User");}
}else{
	die("Didn't got the right DATA");
}
?>