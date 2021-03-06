<?php
function go_to_log_in($status){
    header('Location: https://yadcapital.com/admin/login'.$status);
    echo 'log in falid';
    die('login2');
}

if ( !isset($_POST['thisPS']) || !isset($_POST['thisUS'])){
	go_to_log_in('');
}

$fileName = 'datafile.json';
$contents = file_get_contents('../data/'.$fileName);

$data = json_decode($contents,true);

if ($_POST['thisPS'] != $data['password'][0] || $_POST['thisUS'] != $data['username'][0]){
 	go_to_log_in('?status=wrong');
}

// $cookie_name = "jsonData";
// $cookie_value = $contents;
// //setcookie($cookie_name, str_replace('\n',"<br>",$contents), time()+1500);
// $compressedJSON = gzdeflate($json, 9);
// setcookie('json', $compressedJSON);
?>

<!DOCTYPE html>
<html>
<head>
    <title>Render Page</title>
    <meta charset="utf-8"/>
    <meta content="Administration render page" name="description">
    <meta content="width=device-width, minimum-scale=1.0, maximum-scale=1.0" name="viewport"/>
    <!--jQuery-->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <!--bootstrap-->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
    <!--bootstrap -> font awesome-->
  	<link href="//maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <!--icons-->
    <link rel="icon" href="../images/ico_small.jpg" type="image/x-icon">
  	<link rel="shortcut icon" href="../images/ico_small.jpg" type="image/x-icon">
  	<!--css-->
    <link rel="stylesheet" href="../files/admin.css?v=0.3">
    <style type="text/css">

    </style>
</head>
<body>
<div class="container" id="description_container">
  <h3>Text description:</h3>    
  <div id="description_p_container">
      <p>normal..</p>  
      <p><strong>{Bold}</strong></p>
      <p><u>{{underline}}</u></p>
      <p><i>[italic]</i></p>
      <p><strong><i>{[strong & italic]}</i></strong></p>
      <p><u><i>{{[underline & italic]}}</i></u></p>   
  </div>
</div>
<form action="javascript:;" id="theForm">
    <div id="form_body">
        <input required="yes" type="hidden" name="oldPs" value="<?php echo $data['password'][0]; ?>">
        <input required="yes" type="hidden" name="oldUs" value="<?php echo $data['username'][0]; ?>">
        <div class="form-group">
            <div class="page_title">Log in page</div>
            <label >User deails
            </label><input required="yes" type="text" class="form-control" name="username" placeholder="Enter username" title="username" value="" style="width:49%; margin-right:1%;"><input required="yes" type="password" class="form-control" name="password" title="password" placeholder="Enter password" value="" style="width:50%;">
        </div>
        <div class="form-group">
            <div class="page_title">Legal Disclaimer</div>
            <label>Legal Disclaimer text</label>
            <textarea required="yes" class="form-control" onkeydown="autosize(this)" placeholder="Enter paragrapt" name="legal_disclaimer"></textarea>
        </div>
        <div class="form-group">
            <div class="page_title">About</div>
            <label>Info text</label>
            <textarea required="yes" class="form-control" onkeydown="autosize(this)" placeholder="Enter paragrapt" name="about"></textarea>
        </div>
        <div class="form-group">
            <div class="page_title">Merchant Cash Advance</div>
            <label>MCA head</label>
            <div class="form_box_container" id="mca_head_box"><!--
                <div class="form_box_input"><div class="form_box_input_data"><textarea required="yes" class="form-control" onkeydown="autosize(this)" placeholder="Enter paragrapt" name="mca_head_paragraph"></textarea></div><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button></div>
             --></div>
            <button class="btn btn-secondary" type="button" onclick="add_box_input('mca_head_box')">Add MCA paragraph</button>
            <label>MCA Funding</label>
            <div class="form_box_container" id="mca_funding_box"><!--
                <div class="form_box_input"><div class="form_box_input_data"><input required="yes" type="text" class="form-control" name="mca_funcding_title" placeholder="Enter title" title="mca_funcding_title" value=""><textarea required="yes" class="form-control" onkeydown="autosize(this)" placeholder="Enter paragrapt" name="mca_funcding_paragraph"></textarea></div><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button></div>
             --></div>
            <button class="btn btn-secondary" type="button" onclick="add_box_input('mca_funding_box')">Add MCA funding</button>
            <label>MCA Balls</label>
            <div class="form_box_container" id="mca_ball_box"><!--
                <div class="form_box_input"><div class="form_box_input_data"><input required="yes" type="text" class="form-control" name="mca_ball_title" placeholder="Enter title" title="mca_ball_title" value="" style="width: 49%; margin-right:1%;"><input required="yes" type="text" class="form-control" name="mca_ball_text" placeholder="Enter text" title="mca_ball_text" value="" style="width: 50%;"></div><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button></div>
             --></div>
            <button class="btn btn-secondary" type="button" onclick="add_box_input('mca_ball_box')">Add MCA ball</button>
        </div>
        <div class="form-group">
            <div class="page_title">Real Estate Debt</div>
            <label>RED head</label>
            <div class="form_box_container" id="red_head_box"><!--
                <div class="form_box_input"><div class="form_box_input_data"><textarea required="yes" class="form-control" onkeydown="autosize(this)" placeholder="Enter paragrapt" name="red_head_paragraph"></textarea></div><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button></div>
             --></div>
            <button class="btn btn-secondary" type="button" onclick="add_box_input('red_head_box')">Add RED paragraph</button>
            <label>RED cards</label>
            <div class="form_box_container" id="red_card_box"><!--
                <div class="form_box_input"><div class="form_box_input_data"><input required="yes" type="text" class="form-control" name="red_card_title" placeholder="Enter title" title="red_card_title" value="" style="width: 49%; margin-right:1%;"><input required="yes" type="text" class="form-control" name="red_card_text" placeholder="Enter text" title="red_card_text" value="" style="width: 50%;"><input required="yes" type="text" class="form-control" name="red_card_bottom" placeholder="Enter bottom text" title="red_card_bottom" value="" style="width: 49%; margin-right:1%;"></div><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button></div>
             --></div>
            <button class="btn btn-secondary" type="button" onclick="add_box_input('red_card_box')">Add RED cards</button>
        </div>
        <div class="form-group">
            <div class="page_title">Team</div>
            <label>Team cards</label>
            <div class="form_box_container" id="team_card_box"><!--
                <div class="form_box_input"><div class="form_box_input_data"><input required="yes" type="url" class="form-control" name="team_card_img" placeholder="Enter image url" title="team_card_img" value=""><input required="yes" type="text" class="form-control" name="team_card_name" placeholder="Enter full name" title="team_card_name" value="" style="width: 49%; margin-right:1%;"><input required="yes" type="text" class="form-control" name="team_card_title" placeholder="Enter full title" title="team_card_title" value="" style="width: 50%;"><input required="yes" type="url" class="form-control" name="team_card_linkedin" placeholder="Enter linkedin URL" title="team_card_linkedin" value="" style="width: 49%; margin-right:1%;"><input required="yes" type="email" class="form-control" name="team_card_email" placeholder="Enter email address" title="team_card_email" value="" style="width: 50%;"><textarea required="yes" class="form-control" onkeydown="autosize(this)" placeholder="Enter BIO" name="team_card_bio"></textarea></div><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button></div>
             --></div>
            <button class="btn btn-secondary" type="button" onclick="add_box_input('team_card_box')">Add Team cards</button>
        </div>
        <div class="form-group">
            <div class="page_title">Press Release</div>
            <label>Press section</label>
            <div class="form_box_container" id="press_section_box"><!--
                <div class="form_box_input"><div class="form_box_input_data"><textarea required="yes" class="form-control" onkeydown="autosize(this)" placeholder="Enter data" name="press_section_data"></textarea><input required="yes" type="url" class="form-control" name="press_section_url" placeholder="Enter read more url" title="press_section_url" value=""><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button></div>
                </div>
             --></div>
            <button class="btn btn-secondary" type="button" onclick="add_box_input('press_section_box')">Add press section</button>
        </div>
        <div class="form-group">
            <div class="page_title">Contact</div>
            <label>Contact emails</label>
            <div class="form_box_container" id="contact_email_box"><!--
                <div class="form_box_input"><div class="form_box_input_data"><input required="yes" type="email" class="form-control" name="contact_email_mail" placeholder="Enter email address" title="contact_email_mail" value="">
                <input required="yes" type="text" class="form-control" name="address_text" placeholder="Enter address text" title="address_text" value="" style="width:49%; margin-right:1%;"><input required="yes" type="text" class="form-control" name="address_pointer" title="address_pointer" placeholder="Enter pointer (example: 40.7629384,-73.978958)" value="" style="width:50%;">
                <button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button></div>
                </div>
             --></div>
            <button class="btn btn-secondary" type="button" onclick="add_box_input('contact_email_box')">Add contact email</button>
        </div>
    </div><footer><div id="footer_button_container"><button type="submit" class="btn btn-info" onclick="download_data()" title="Download data"><i class="fa fa-cloud-download"></i></button><button type="button" class="btn btn-info" onclick="upload_data()" title="Upload data"><i class="fa fa-upload"></i></button><button type="submit" class="btn btn-info" onclick="update_data('json')" title="Save data"><i class="fa fa-floppy-o"></i></button><button type="submit" class="btn btn-info" onclick="update_data('test')">Test</button><button type="submit" class="btn btn-info" onclick="update_data('production')">Product</button></div></footer>
</form>
<!-- <footer><div id="footer_button_container"><button type="submit" class="btn btn-info" onclick="download_data()">Download data</button><button type="button" class="btn btn-info" onclick="upload_data()">Upload data</button><button type="submit" class="btn btn-info" onclick="update_data('json')">Save data</button><button type="submit" class="btn btn-info" onclick="update_data('test')">Update test</button><button type="submit" class="btn btn-info" onclick="update_data('production')">Update production</button></div></footer> -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
<script src="../files/jquery.cookie.js"></script>
<script type="text/javascript">
//$("textarea").each(function(){autosize(this);});

function autosize(el){
  setTimeout(function(){
    el.style.cssText = 'height:auto; padding:0';
    // for box-sizing other than "content-box" use:
    // el.style.cssText = '-moz-box-sizing:content-box';
    el.style.cssText = 'height:' + (el.scrollHeight+14) + 'px';
  },0);
}
var data = {
	'mca_head_box':'<div class="form_box_input_data"><textarea required="yes" class="form-control" onkeydown="autosize(this)" placeholder="Enter paragrapt" name="mca_head_paragraph"></textarea></div><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button>',
    'mca_funding_box':'<div class="form_box_input_data"><input required="yes" type="text" class="form-control" name="mca_funcding_title" placeholder="Enter title" title="mca_funcding_title" value=""><textarea required="yes" class="form-control" onkeydown="autosize(this)" placeholder="Enter paragrapt" name="mca_funcding_paragraph"></textarea></div><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button>',
    'mca_ball_box':'<div class="form_box_input_data"><input required="yes" type="text" class="form-control" name="mca_ball_title" placeholder="Enter amount" title="mca_ball_title" value="" style="width: 49%; margin-right:1%;"><input required="yes" type="text" class="form-control" name="mca_ball_text" placeholder="Enter text" title="mca_ball_text" value="" style="width: 50%;"></div><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button>',
    'red_head_box':'<div class="form_box_input_data"><textarea required="yes" class="form-control" onkeydown="autosize(this)" placeholder="Enter paragrapt" name="red_head_paragraph"></textarea></div><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button>',
    'red_card_box':'<div class="form_box_input_data"><input required="yes" type="text" class="form-control" name="red_card_title" placeholder="Enter title" title="red_card_title" value="" style="width: 49%; margin-right:1%;"><textarea required="yes" class="form-control" onkeydown="autosize(this)" placeholder="Enter middel text" name="red_card_text"></textarea>'+'<textarea required="yes" class="form-control" onkeydown="autosize(this)" placeholder="Enter bottom text" name="red_card_bottom"></textarea></div><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button>',
    'team_card_box':'<div class="form_box_input_data"><input required="yes" type="text" class="form-control" name="team_card_img" placeholder="Enter image url" title="team_card_img" value=""><input required="yes" type="text" class="form-control" name="team_card_name" placeholder="Enter full name" title="team_card_name" value="" style="width: 49%; margin-right:1%;"><input required="yes" type="text" class="form-control" name="team_card_title" placeholder="Enter full title" title="team_card_title" value="" style="width: 50%;"><input required="yes" type="url" class="form-control" name="team_card_linkedin" placeholder="Enter linkedin URL" title="team_card_linkedin" value="" style="width: 49%; margin-right:1%;"><input required="yes" type="email" class="form-control" name="team_card_email" placeholder="Enter email address" title="team_card_email" value="" style="width: 50%;"><textarea required="yes" class="form-control" onkeydown="autosize(this)" placeholder="Enter BIO" name="team_card_bio"></textarea></div><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button>',
    'press_section_box':'<div class="form_box_input_data"><textarea required="yes" class="form-control" onkeydown="autosize(this)" placeholder="Enter data" name="press_section_data"></textarea><input required="yes" type="url" class="form-control" name="press_section_url" placeholder="Enter read more url" title="press_section_url" value=""><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button>',
    'contact_email_box':'<div class="form_box_input_data"><input required="yes" type="email" class="form-control" name="contact_email_mail" placeholder="Enter email address" title="contact_email_mail" value=""><input required="yes" type="text" class="form-control" name="address_text" placeholder="Enter address text" title="address_text" value="" style="width:49%; margin-right:1%;"><input required="yes" type="text" class="form-control" name="address_pointer" title="address_pointer" placeholder="Enter pointer (example: 40.7629384,-73.978958)" value="" style="width:50%;"><button class="btn btn-danger" type="button" onclick="delete_box_input(this)">X</button>',
}
var title_to_key={
    'mca_head_paragraph':'mca_head_box',
    'mca_funcding_title':'mca_funding_box',
    'mca_funcding_paragraph':'mca_funding_box',
    'mca_ball_title':'mca_ball_box',
    'mca_ball_text':'mca_ball_box',
    'red_head_paragraph':'red_head_box',
    'red_card_title':'red_card_box',
    'red_card_text':'red_card_box',
    'red_card_bottom':'red_card_box',
    'team_card_img':'team_card_box',
    'team_card_name':'team_card_box',
    'team_card_title':'team_card_box',
    'team_card_linkedin':'team_card_box',
    'team_card_email':'team_card_box',
    'team_card_bio':'team_card_box',
    'press_section_data':'press_section_box',
    'press_section_url':'press_section_box',
    'contact_email_mail':'contact_email_box',
    'address_text':'contact_email_box',
    'address_pointer':'contact_email_box',
}
function validForm() {
	var form = document.getElementById('theForm');
    for(var i=0; i < form.elements.length; i++){
        if(form.elements[i].value === '' && form.elements[i].hasAttribute('required')){
            return false;
        }
    }
	return true;
}
function delete_box_input(argument) {
    a = argument;
    var parent = argument.parentElement;
    parent.remove();
}
function add_box_input(id) {
     div = document.createElement("DIV");
     div.classList.add("form_box_input");
     div.innerHTML = data[id];
     document.getElementById(id).appendChild(div);
 }

function objectifyForm(formArray) {//serialize data function

  var returnArray = {};
  for (var i = 0; i < formArray.length; i++){
    if (!(formArray[i]['name'] in returnArray))
        returnArray[formArray[i]['name']] = []
    returnArray[formArray[i]['name']].push(formArray[i]['value']);
  }
  return returnArray;
}
 function form_to_json(){
    formArray = $( "form" ).serializeArray();
    json_data = objectifyForm(formArray);
    return json_data;

 }
 function download_data(){
 	if (validForm()){
	    json_data = form_to_json();
	    delete json_data["oldPs"];
	    delete json_data["oldUs"];
	    myJSON = JSON.stringify(json_data);
	    downloadFile("datafile.json",myJSON);
	}
 }

 function downloadFile(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}
var add_as_box;
function json_to_form(json_data){
    add_as_box = {};
    for(var title in json_data) {
        if (title in title_to_key)
        {
            box_name = title_to_key[title];
            if (!(box_name in add_as_box))
                add_as_box[box_name] = {'len':-1};
            if (!(title in add_as_box[box_name]))
                add_as_box[box_name][title] = [];
            for (var i in json_data[title]){
                txtData = json_data[title][i];
                add_as_box[box_name][title].push(txtData);
                add_as_box[box_name]['len'] = Math.max(add_as_box[box_name]['len'],add_as_box[box_name][title].length);
            }
        }
        else
        {
            txtData = json_data[title][0];
            $('[name="'+title+'"]')[0].value=txtData;
        }
    }

    for (var box_name in add_as_box){
        box_data = add_as_box[box_name];
        document.getElementById(box_name).innerHTML="";
        box_html = data[box_name];
        var len = box_data['len'];
        for (var i=0;i<len;i++){
            div = document.createElement("DIV");
            div.classList.add("form_box_input");
            div.innerHTML = box_html;
            for (var title in box_data){
                if (title != "len")
                {
                    div.querySelector('[name="'+title+'"]').value=box_data[title][i];
                }
            }
            document.getElementById(box_name).appendChild(div);
        }
    }
    $("textarea").each(function(){autosize(this);});

}

function openFile(event) {
        var input = event.target;
        var reader = new FileReader();
        reader.onload = function(){
          myJSON = reader.result;
          json_data = JSON.parse(myJSON);
          json_to_form(json_data);
        };
        reader.readAsText(input.files[0]);
};

function upload_data(){
    var element = document.createElement('input');
    element.setAttribute('type', "file");
    element.setAttribute('accept', "text/json");
    element.setAttribute('onchange', "openFile(event)");
    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}
var sendData;
function update_data(actionOn){
    if (validForm()){
        json_data = form_to_json();
        json_data['actionOn'] = actionOn;
        // Sending and receiving data in JSON format using POST method
        //
        var xhr = new XMLHttpRequest();
        var url = "https://yadcapital.com/data/handel.php";
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                res = JSON.parse(xhr.responseText);
                alert(res['posts']);
            }
        };
        sendData = JSON.stringify(json_data);
        sendData = sendData.split("\\r\\n").join("<br>");
        xhr.send(sendData);
    }
}

$(document).ready(function() {
	myJSON = "<?php
	$cookie_value = str_replace('\n',"\\r\\n",$contents);
	$cookie_value = str_replace('"','\\"',$cookie_value);
	echo $cookie_value;
	?>";
	myJSON = myJSON.split("\r\n").join("\\r\\n");
	json_data = JSON.parse(myJSON);
	json_to_form(json_data);
	$("textarea").each(function(){autosize(this);});
    // if  ($.cookie("jsonData")){
    //   myJSON =  $.cookie("jsonData");
    //   json_data = JSON.parse(myJSON);
    //   json_to_form(json_data);
    //   $("textarea").each(function(){autosize(this);});
    // }
});

 //  TODO make all the fucntions of the button above.

 // to make form -> json (and then download/ send it)
 // https://stackoverflow.com/questions/1184624/convert-form-data-to-javascript-object-with-jqueryssפיפ
</script>
</body>
</html>