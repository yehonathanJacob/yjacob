<?php
if ( !isset($_GET['thisPS']) || !isset($_GET['thisUS'])){
	go_to_log_in();
}
else{
	if ( ($_GET['thisUS']!="test" || $_GET['thisPS']!="admin") && ($_GET['thisUS']!="prod" || $_GET['thisPS']!="admin"))
		go_to_log_in();
	else{
		echo 'hello world';
	}
}
function go_to_log_in(){
    header('Location: https://yadcapital.com/admin/login');
    echo 'log in falid';
    die('login2');
}
$fileName = $_GET['thisUS'].'.json';
$contents = file_get_contents('../data/'.$fileName);
$data = json_decode($contents, true);
?>
<?php
echo "message: ".$data['message']."<br>array: ";
print_r($data['array']);
?>