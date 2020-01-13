<?php
if ( !isset($_POST['thisPS']) || !isset($_POST['thisUS'])){
	go_to_log_in();
}

if ( $_POST['thisUS']!="test" && $_POST['thisUS']!="prod" ){
	go_to_log_in();
}

function go_to_log_in(){
    header('Location: https://yadcapital.com/admin/login');
    echo 'log in falid';
    die('login2');
}

$fileName = $_POST['thisUS'].'.json';
$contents = file_get_contents('../data/'.$fileName);
$data = json_decode($contents, true);
if ($_POST['thisPS'] != $data['password']){
 	go_to_log_in();
}
?>
<?php
echo "message: ".$data['message']."<br>array: ";
print_r($data['array']);
for ($i =0; $i < count($data['array']);$i++){
	echo "<p>var: ".$data['array'][$i]."</p>";
}
// if ( !isset($_POST['thisPS']) || !isset($_POST['thisUS'])){
// 	go_to_log_in();
// }

// if ( ($_POST['thisUS']!="test" &&  $_POST['thisUS']!="prod"))
// 	go_to_log_in();

// $fileName = $_POST['thisUS'].'.json';
// echo $fileName;
// $contents = file_POST_contents('../data/'.$fileName);
// $data = json_decode($contents, true);

// if ($_POST['thisPS'] != $data['password'])
// 	go_to_log_in();

// function go_to_log_in(){
//     header('Location: https://yadcapital.com/admin/login');
//     echo 'log in falid';
//     die('login2');
// }

// ?>
<?php
// echo "message: ".$data['message']."<br>array: ";
// for ($i =0; $i < count($data['array']);$i++)
// 	echo "<p>var: ".$data['array'][$i]."</p>";
// print_r($data['array']);
?>