<?php
if(isset($_POST['User'])&&isset($_POST['Ps']))
{
	checkPage();
	$conn = new mysqli("sql145.main-hosting.eu.", "u976997437_sm", "WfkNBBNMrbp4", "u976997437_msqlp");
	if ($conn->connect_error) {
		$conn->close();
		die("Connection failed: " . $conn->connect_error);}
	$user = $conn->real_escape_string(htmlentities($_POST['User']));
	$ps = $conn->real_escape_string(htmlentities($_POST['Ps']));
	$check="False";
	$result = $conn->query('SELECT * FROM MyUsers');
	while($object = $result->fetch_object()){
		if((strtolower($user)==strtolower($object->UserName))&&(strtolower($ps)==strtolower($object->Password))){
				$check="True";
				$zwhrh6DgKl=$user;
				$pss = $ps;
		}
	}
	$conn->close();
}
else{header('Location: index.html');}

function checkPage(){
if(!isset($_POST["g-recaptcha-response"])){die("Hello Bots");}//if it is a robot it will stop hear.
$url = 'https://www.google.com/recaptcha/api/siteverify';
//Type in secret your secert Key
$data = array('secret' => '6LdTOBgUAAAAAEPfWQv1UMOUiiPlFLBVzBsJQ74V', 'response' => $_POST["g-recaptcha-response"]);//this is the post value arriver from the html page

// use key 'http' even if you send the request to https://...
$options = array(
    'http' => array(
        'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
        'method'  => 'POST',
        'content' => http_build_query($data)
    )
);

$context  = stream_context_create($options);
$result = file_get_contents($url, false, $context);
if ($result === FALSE) { die("Error In Google Recaptcha"); }
$json = json_decode($result, true);//json To Arry
if(!$json['success']){die("You Didn't Clike on 'I am not a robot");}//if he didn't clike, it will stop hear.
}
?>
<!DOCTYPE html>
<html>
<head>
	<title>MyLocker</title>
	<!--Hebrew-->
	<meta charset="utf-8"/>
	<!--Responsiv-->
	<meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0" />
	<script type="text/javascript" src="https://code.jquery.com/jquery-latest.min.js"></script>
	<!--font awesome from folder-->
	<link rel="stylesheet" href="font-awesome-4.2.0/css/font-awesome.css">
	<!--CSS Style-->
	<link rel="stylesheet" type="text/css" href="common.css">
	<link rel="stylesheet" type="text/css" href="home.css">
	<!--logo MyLocker-->
	<link rel="icon" href="logoMyLocker.png" type="image/x-icon">
	<link rel="shortcut icon" href="logoMyLocker.png" type="image/x-icon">
</head>
<body>
<!--google analytics-->
<?php include_once("analyticstracking.php") ?>
<?php if(isset($zwhrh6DgKl)){echo '<input style="display:none;" type="hidden" id="null" value="'.$user.'|'.$pss.'">';} ?>
	<div id="top"><div id="title" title="My Locker"><i class="fa fa-lock" ></i><span> <?php 
	if(isset($zwhrh6DgKl))
		echo $zwhrh6DgKl;
	?></span></div></div>
	<div id="topBar">
		<span id="ControlBarI">
			<i id="ControlI" class="fa fa-cog"></i>
			<div id="ControlBar"><button id="DeleteAccount" class="Red" title="Delete Account">
					<i class="fa fa-ban"></i>
				</button><a href="index.html" class="Red" id="LogOutB" title="Log Out">
					<i class="fa fa-sign-out"></i>
				</a><button id="NewPsB" title="New Password">
					<i class="fa fa-plus-square"></i>
				</button><button id="Refresh" title="Refresh Data">
					<i class="fa fa-refresh"></i>
  				</button></div></span><input type="search" placeholder="Search Type" name="Search" title="Type search"><button id="SearchB" title="Search Button">
		<i class="fa fa-search"></i></button>
	</div>
	<table title="Table">
	<thead>
		<tr class="top">
			<td class="Control" title="Control Button"></td>
			<td class="type" title="Type">Type</td>
			<td class="ps" title="Password">Password</td>
		</tr>
	</thead>
	<tbody>
		<?php
		if(isset($zwhrh6DgKl))
		{
			$conn2 = new mysqli("sql145.main-hosting.eu.", "u976997437_sm", "WfkNBBNMrbp4", "u976997437_msqlp");
			if ($conn2->connect_error) {
				$conn2->close();
				die("Connection failed: " . $conn2->connect_error);}
			else{
				$conut=0;
				$result2 = $conn2->query('SELECT * FROM '.strtolower($zwhrh6DgKl).'');
				while($object2 = $result2->fetch_object()){
					$conut = $object2->id;
					echo '<tr id="tr'.$conut.'">';
					echo '<td class="Control" title="Control Button"><i id="ok'.$conut.'" class="fa fa-floppy-o"></i><i id="dele'.$conut.'" class="fa fa-trash-o"></i></td>';
					echo '<td class="type" title="Type"><input type="text" name="TypeText" value="'.$object2->Type.'"></td>';
					echo '<td class="ps" title="Password"><i id="lockPs'.$conut.'" class="fa fa-lock"></i><i id="UnlockPs'.$conut.'" class="fa fa-unlock-alt"></i><input id="Ps'.$conut.'" type="text" value="'.$object2->Password.'"><textarea id="txPs'.$conut.'">'.$object2->Details.'</textarea></td>';
					echo "</tr>";
				}
				$conn2->close();
			}
		}
		else{
			echo "didn't find";
		}
		?>
	</tbody>
	</table><span id="AddNewPS">
		<h3>New Password</h3>
		<form title="New Password" action="">
			<input class="NormalText" style="text-algin: center;" name="Type" type="text" placeholder="Type" title="Type">
			<input class="onlyEng" style="text-algin: center;" name="Ps" type="password" placeholder="Passworrd" title="Passworrd">
			<input class="onlyEng" style="text-algin: center;" name="RePs" type="password" placeholder="Re-Passworrd" title="RePassworrd">
			<textarea rows="5" style="margin: 1%; padding:1%; border-radius:2px; " placeholder="Details"></textarea>
			<input type="button" id="NePSbutton" value="Add" onclick="AdNePs()">
		</form>
	</span>
	<footer><div id="copyright"><i class="fa fa-copyright" aria-hidden="true"></i><a href="http://all-in-one.cf">All In One</a></div> </footer>
<script type="text/javascript">	
	var ul= $('#top #title span');
	$('#top #title').click(function(){
		if(ul.css('display') == 'inline-block')
		{
			ul.hide(300);
		}
		else{
			ul.show(300);
		}
	});
	$('.onlyEng').bind('keypress', function (event) {
	    var regex = new RegExp("^[a-zA-Z0-9א-ת]+$");
	    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
	    if (!regex.test(key)) {
	alert('you can type her only\n a-z A-Z 0-9 א-ת');
	       event.preventDefault();
	       return false;
	    }
	});
	$('.NormalText').bind('keypress', function (event) {
	    var regex = new RegExp("^[a-zA-Z0-9א-ת ]+$");
	    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
	    if (!regex.test(key)) {
	alert('you can type her only\n a-z A-Z 0-9 א-ת " "]');
	       event.preventDefault();
	       return false;
	    }
	});
</script>
<script type="text/javascript" src="home.js"></script>
</body>
</html>