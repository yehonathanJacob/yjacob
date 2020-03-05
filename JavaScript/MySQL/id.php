<?php 

$mysqli = new mysqli("mysql.hostinger.co.il", "u528924860_sm", "WfkNBBNMrbp4", "u528924860_msqlp");

$id = $mysqli->real_escape_string(htmlentities($_GET['id']));
echo 'id=<br>'.$id.'<br>'.$_GET['id'];
$result = $mysqli->query("SELECT * FROM MyUsers WHERE id=$id");

echo $result->fetch_object()->UserName;

?>