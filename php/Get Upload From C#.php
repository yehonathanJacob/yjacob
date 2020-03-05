<?php
$uploads_dir = './files'; //Directory to save the file that comes from client application.
if ($_FILES["file"]["error"] == UPLOAD_ERR_OK) {
    $tmp_name = $_FILES["file"]["tmp_name"]; //the original file name
    $name = $_FILES["file"]["name"]; //name that you wnat the file will have
    move_uploaded_file($tmp_name, "$uploads_dir/$name");
}
?>