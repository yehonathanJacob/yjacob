<?php include_once("analyticstracking.php") ?>
<?php
$amount;
if(isset($_POST['Fun']))
{
  $FunName = htmlentities($_POST['Fun']);
  switch($FunName){
    case "sendMessage":
      sendMessage();
      break;
    case "paymentById":
      paymentById();
      break;
		case "paymentByForm":
			paymentByForm();
			break;
    default:
        die("This fanction dosen't exists");
  }
}else{
  die("didn't get function name");
}
function sendMessage(){
  if(isset($_POST['messsage'])&&isset($_POST['topic']))
  {
    $message = htmlentities($_POST['messsage']);
    $topic = htmlentities($_POST['topic']);
    if(mail("Allin1.16mb@gmail.com","Mail from All In One client: ".$topic,$message) == 1){echo "True";}
  }
  else{die("didn't get right function details");}
}
function paymentById(){
  if(isset($_POST['id']))
  {
    $conn = new mysqli("mysql.hostinger.co.il", "u219898780_usai1", "3bFczdVbkoe", "u219898780_ai1");
    if ($conn->connect_error) {
		  $conn->close();
		die("Connection failed: " . $conn->connect_error);}
    $paymentId = $conn->real_escape_string(htmlentities($_POST['id']));
    $result = $conn->query('SELECT * FROM payments WHERE id='.$paymentId.'');
    $object = $result->fetch_object();
    if(!$object)
    {
      die('False');
    }else{                  
      $html = GetForm($object);
      die($html);
    }
    
  }else{die("method is missing");}
}
function paymentByForm(){
	if(isset($_POST['firstName'])&&isset($_POST['lastName'])&&isset($_POST['night_phone_a'])&&isset($_POST['address1'])&&isset($_POST['address2'])&&isset($_POST['city'])&&isset($_POST['state'])&&isset($_POST['email'])&&isset($_POST['amount'])){
		$conn = new mysqli("mysql.hostinger.co.il", "u219898780_usai1", "3bFczdVbkoe", "u219898780_ai1");
    if ($conn->connect_error) {
		  $conn->close();
		die("False Connection failed: " . $conn->connect_error);}
		$sql ="INSERT INTO payments (firstName, lastName, phone, address1, address2, city, state, email, amount, payed) VALUES (
		'".$conn->real_escape_string(htmlentities($_POST['firstName']))."',
		'".$conn->real_escape_string(htmlentities($_POST['lastName']))."',
		'".$conn->real_escape_string(htmlentities($_POST['night_phone_a']))."',
		'".$conn->real_escape_string(htmlentities($_POST['address1']))."',
		'".$conn->real_escape_string(htmlentities($_POST['address2']))."',
		'".$conn->real_escape_string(htmlentities($_POST['city']))."',
		'".$conn->real_escape_string(htmlentities($_POST['state']))."',
		'".$conn->real_escape_string(htmlentities($_POST['email']))."',
		'".$conn->real_escape_string(htmlentities($_POST['amount']))."',
		'False'
		)";
		if ($conn->query($sql) === TRUE) {
			$LastId = $conn->insert_id;			
			$result = $conn->query('SELECT * FROM payments WHERE id='.$LastId.'');
			$object = $result->fetch_object();
			$html = GetForm($object);
      die($html);
		} else {
			die("False ".$sql . "\n" . $conn->error);
		}
		
	}else{die("False Data is missing");}	
}
function GetForm($object){  
  $URLBake = 'http://allin1.16mb.com/payments.php?ps=1234566&id='.$paymentId.'';      
	$paymentId = $object->id;
  $amount = $object->amount;      
  $firstName = $object->firstName;
  $lastName = $object->lastName;
  $address1 = $object->address1;
  $address2 = $object->address2;
  $city = $object->city;
  $state = $object->state;
  $phone = $object->phone;
  $email = $object->email;
	
  $form = "";
  $form = $form.'<form action="https://www.paypal.com/cgi-bin/webscr" method="post">';
  $form = $form.'\n<input type="hidden" name="cmd" value="_xclick">';  
  $form = $form.'\n<input TYPE="hidden" name="charset" value="utf-8">';
  $form = $form.'\n<input TYPE="hidden" name="return" value="'.$URLBake.'">';
  $form = $form.'\n<input type="hidden" name="business" value="janjak2411@gmail.com">';
  $form = $form.'\n<input type="hidden" name="item_name" value="תשלום בעבור מתן שירות">';
  $form = $form.'\n<input type="hidden" name="item_number" value="'.$paymentId.'">';	
  $form = $form.'\n<input type="hidden" name="amount" value="'.$amount.'">';
	$form = $form.'\n<input type="hidden" name="currency_code" value="ILS">';
	$form = $form.'\n<input type="hidden" name="address_override" value="1">';
  $form = $form.'\n<input type="hidden" name="first_name" value="'.$firstName.'">';
  $form = $form.'\n<input type="hidden" name="last_name" value="'.$lastName.'">';
  $form = $form.'\n<input type="hidden" name="address1" value="'.$address1.'">';
  $form = $form.'\n<input type="hidden" name="address2" value="'.$address2.'">';
  $form = $form.'\n<input type="hidden" name="city" value="'.$city.'">';
  $form = $form.'\n<input type="hidden" name="state" value="'.$state.'">';
	$form = $form.'\n<input type="hidden" name="country" value="IL">';
  $form = $form.'\n<input type="hidden" name="night_phone_a" value="'.$phone.'">';
  $form = $form.'\n<input type="hidden" name="email" value="'.$email.'">';
  $form = $form.'\n<input type="image" name="submit" alt="PayPal - The safer, easier way to pay online">';
  $form = $form.'\n</form>';
  return $form;
}
?>