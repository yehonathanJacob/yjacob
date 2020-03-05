<!--simpel MySQL-->
<?php 

$mysqli = new mysqli('mysql.hostinger.co.il', 'u614295215_admin', 'admin123', 'u614295215_check');

$result = $mysqli->query('SELECT * FROM Students');

$tabel = [];
$row = [];

while($object = $result->fetch_object()){
	$row[] = $object->id;
	$row[] = $object->name;
	$row[] = $object->age;
	$table[] = $row;
	$row = [];
}

echo var_dump($table);
echo "<br>first ID: ".$table[0][0]."<br>FirstName: ".$table[0][1]."<br>lastAge: ".$table[1][2];
 ?>
 <!--Class of MySQL-->
 <?php 
$mysqli = new MySqliClass();
$mysqli->RunQuery('gssgea');


if($mysqli->affected_rows)//True if query succeded

class MySqliClass
{
	public $mysqli;

	function __construct(){
		$this->mysqli = new mysqli('localhost', 'stagadis_admin', 'stagadish', 'stagadis_project');
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
<!--MySQL Ingeckshen-->
<?php 

$mysqli = new mysqli('mysql.hostinger.co.il', 'u614295215_admin', 'admin123', 'u614295215_check');

$id = $mysqli->real_escape_string(htmlentities($_GET['id']));

$result = $mysqli->query("SELECT * FROM Students WHERE id=$id");

echo $result->fetch_object()->name;
?>