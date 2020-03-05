<?php
if(isset($_POST['User'])&&isset($_POST['Ps'])&&isset($_POST['Email']))
{
	$conn = new mysqli("sql145.main-hosting.eu.", "u976997437_sm", "WfkNBBNMrbp4", "u976997437_msqlp");
	if ($conn->connect_error) {
		$conn->close();
		die("Connection failed: " . $conn->connect_error);}
	$result = $conn->query('SELECT * FROM MyUsers');
	while($object = $result->fetch_object()){
		if(strtolower($_POST['User'])==strtolower($object->UserName))
			{$conn->close();
			die("Please try another User Name");}
	}
	$sql ="INSERT INTO MyUsers (UserName, Password, Email)
	VALUES ('".$_POST['User']."','".$_POST['Ps']."','".$_POST['Email']."')";
	if ($conn->query($sql) === TRUE) {
		$sqlTable="CREATE TABLE ".strtolower($_POST['User'])." (
		id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
		Type VARCHAR(30) NOT NULL,
		Password VARCHAR(30) NOT NULL,
		Details MEDIUMTEXT NOT NULL,
		reg_date TIMESTAMP
		)";
		if ($conn->query($sqlTable) === TRUE) {
			$conn->close();
    		die("");
		} else {
			$conn->close();
    		die("Error creating table: " . $conn->error);
		}
	} else {
		$conn->close();
	    die("Error: " . $sql . "<br>" . $conn->error);
	}
}
else{
	die("Error with getting info");
}
?>