<?php 
error_reporting(0);


if(!preg_match("/^[0-9]{1,2}$/", $_GET['month']))
{
    // handle error
}
if(!preg_match("/^[0-9]{1,2}$/", $_GET['day']))
{
    // handle error
}
if(!preg_match("/^[0-9]{4}$/", $_GET['year']))
{
    // handle error
}

$mysqli->real_escape_string(htmlentities("STRING", ENT_QUOTES , "UTF-8"));
 ?>