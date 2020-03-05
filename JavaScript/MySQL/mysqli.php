<?php 
$mysqli = new mysqli('mysql.hostinger.co.il', 'u614295215_admin', 'admin123', 'u614295215_check');
$result = $mysqli->query('SELECT * FROM Students');

$array = [];

while($object = $result->fetch_object()){
	$array[] = $object->name.'<br>';
}

echo var_dump($array);

$mysqli = new MySqliClass();
$mysqli->RunQuery('gssgea');


if($mysqli->affected_rows)//True if query succeded

class MySqliClass
{
	public $mysqli;

	function __construct(){
		$this->mysqli = new mysqli('localhost', 'UserName', 'Password', 'DataBase');
		$this->mysqli->set_charset("utf8");
		$this->RunQuery("SET time_zone = 'Israel'");
	}
	
	function RunQuery($sql_query){
		$this->mysqli->query($sql_query);
		if($this->mysqli->affected_rows){
			return true;
		}
		return false;
	}

	function SelectFromDB($sql_query){
		if($result = $this->mysqli->query($sql_query)){
			return $result;
		}
		return 'Error';
	}
}


?>

