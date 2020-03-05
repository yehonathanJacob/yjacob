<?Php

if($_POST['dt']!='')
{
	file_put_contents('text.txt', $_POST['dt']);
	
}
else
{
	echo file_get_contents('text.txt');
}
?>