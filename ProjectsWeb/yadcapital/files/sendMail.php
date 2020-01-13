<?php
if(isset($_POST["To"]) && isset($_POST["Message"]) && isset($_POST["Subject"])){
  if(mail($_POST['To'],$_POST['Subject'],$_POST['Message']))
  {
    echo "Message was sent.";
  }
  else{
    echo "Error in message.";
  }
}else{
  die($_POST["To"].$_POST["Message"].$_POST["Subject"]);
}
?>