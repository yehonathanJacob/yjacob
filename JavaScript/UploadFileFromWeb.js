var file_data = $("#ThisFile").prop('files')[0];   
var form_data = new FormData();                  
$.ajax({
            url: 'UploadFile.php', // point to server-side PHP script
            dataType: 'text',  // what to expect back from the PHP script, if anything
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,                         
            type: 'post',
            success: function(php_script_response){     
              var response = php_script_response; // display response from the PHP script, if any           
            }
});           

/*
<!DOCTYPE html>
<html>
<head>
	<title></title>
</head>
<body>
		<input id="ThisFile" type="file" name="image" accept="image/*">
</body>
</html>
*/