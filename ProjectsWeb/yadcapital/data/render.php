<?php
function celanHTML($Text){
  $Html = str_replace('\n',"<br>",$Text);
  $Html = str_replace("\n","<br>",$Text);
  $Html = str_replace("{{","<u>",$Html);
  $Html = str_replace("}}","</u>",$Html);
  $Html = str_replace("{","<strong>",$Html);
  $Html = str_replace("}","</strong>",$Html);
  $Html = str_replace("[","<i>",$Html);
  $Html = str_replace("]","</i>",$Html);
  return $Html;
}
$fileName = 'datafile.json';
$contents = file_get_contents('../data/'.$fileName);
$jsonData = json_decode($contents, true);
?>
<!DOCTYPE html>
<html sytle="font-size: unset;">
<head>
  <title>YAD Capital</title>
  <base href="<?php echo $args['URL']; ?>">
  <!--<base href="../">-->
  <meta charset="utf-8"/>
  <meta name="description" content="Investment Firm Focused on Alternative Credit Opportunities">
  <!--css-->
  <link rel="stylesheet" href="files/home.css?v=2.1">
  <!--Responsiv-->
  <meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0" />
  <!--font awesome-->
  <script src="https://use.fontawesome.com/9a4307ff22.js"></script>
  <!-- Latest compiled and minified CSS-->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <!--Jquery-->
  <script type="text/javascript" src="https://code.jquery.com/jquery-latest.min.js"></script>
  <link rel="icon" href="images/ico_small.jpg" type="image/x-icon">
  <link rel="shortcut icon" href="images/ico_small.jpg" type="image/x-icon">
  <!--AOS OnScroll -->
  <link href="https://cdn.rawgit.com/michalsnik/aos/2.1.1/dist/aos.css" rel="stylesheet">
</head>
<body>
<header>
  <div id="headerDataContainer">
  <div id="headerData">
    <div></div>
    <img src="images/foolIco.png" alt="YAD Cpital icon">
    <p>Investment Firm Focused on Alternative Credit Opportunities</p>
    <p id="seocnd_p">New York <img id="diamond_svg" src="images/diamond.svg" alt="diamond"> Miami</p>
    <div id="LegalDisclaimerButton" data-toggle="modal" data-target="#LegalDisclaimerModal">Legal Disclaimer</div>
  </div>
  </div>
</header>
<nav>
<img src="images/foolIco.png" alt="YAD Cpital icon">
<div id="menueButton" onclick="navigationOC(this)">
  <div class="bar1"></div>
  <div class="bar2"></div>
  <div class="bar3"></div>
</div><div id="menueContainer"><div id="buttonsContainer"><button type="button" onclick="ScrollTo(this)" id="homeButton">HOME
</button><button onclick="ScrollTo(this)" type="button" id="aboutButton">ABOUT
</button><button onclick="ScrollTo(this)" type="button" id="mcaButton">MCA
</button><button onclick="ScrollTo(this)" type="button" id="RealEsButton">REAL ESTATE
</button><button onclick="ScrollTo(this)" type="button" id="teamButton">TEAM
</button><button onclick="ScrollTo(this)" type="button" id="pressButton">PRESS
</button><button onclick="ScrollTo(this)" type="button" id="contactButton">CONTACT
</button></div></div>
</nav>
<div class="form about"><div data-aos="zoom-in" class="Ftitle">
</div><p data-aos="fade-up" class="dataText"><?php
echo celanHTML($jsonData['about'][0]);
?></p></div><div class="form mca"><div data-aos="zoom-in" class="Ftitle">Merchant Cash Advance
</div><div data-aos="fade-up" class="dataText"><?php
if (isset($jsonData['mca_head_paragraph'])){
  for ($i =0; $i < count($jsonData['mca_head_paragraph']);$i++){
    echo "<p>".celanHTML($jsonData['mca_head_paragraph'][$i])."</p>";
  }
}
?>
</div>
<div class="TextContainer"><?php
if (isset($jsonData['mca_funcding_title'])){
  for ($i =0; $i < count($jsonData['mca_funcding_title']);$i++){
    echo "<p data-aos='fade-up' class='dataText'>".celanHTML($jsonData['mca_funcding_title'][$i])."<br>".celanHTML($jsonData['mca_funcding_paragraph'][$i])."</p>";
  }
}
?></div><div id="MCA_circels"><?php
if (isset($jsonData['mca_ball_title'])){
  for ($i =0; $i < count($jsonData['mca_ball_title']);$i++){
    echo "<div class='circel_box'><div class='circel_container' data-aos='fade-up'><span class='circel_content'>".celanHTML($jsonData['mca_ball_title'][$i]).celanHTML($jsonData['mca_ball_text'][$i])."</span></div></div>";
  }
}
?></div>
</div><div class="form RealEs"><hr data-aos="zoom-in"><div data-aos="zoom-in" class="Ftitle">Real Estate Debt
</div>
<div data-aos="fade-up" class="dataText"><?php
if (isset($jsonData['red_head_paragraph'])){
  for ($i =0; $i < count($jsonData['red_head_paragraph']);$i++){
    $text_align = (stripos($jsonData['red_head_paragraph'][$i], "    ") !== false)? 'text-align: left;': '';
    echo "<p style='".$text_align."'>".celanHTML($jsonData['red_head_paragraph'][$i])."</p>";
  }
}
?>
</div>
<div class="boxContainer"><?php
if (isset($jsonData['red_card_title'])){
  for ($i =0; $i < count($jsonData['red_card_title']);$i++){
    echo "<div class='box' data-aos='flip-left'><div class='box_title'>".celanHTML($jsonData['red_card_title'][$i])."</div><div class='box_middel'>".celanHTML($jsonData['red_card_text'][$i])."</div><div class='box_bottom'>".celanHTML($jsonData['red_card_bottom'][$i])."</div></div>";
  }
}
?></div>
</div>
<div class="walkingPeople" data-parallax="scroll" data-image-src="images/walkingPeople.jpg">
</div><div class="form team"><div data-aos="zoom-in" class="Ftitle">TEAM
</div><?php
if (isset($jsonData['team_card_img'])){
  for ($i =0; $i < count($jsonData['team_card_img']);$i++){
    echo '<div data-aos="flip-right" class="card"><img class="profilePic" src="'.$jsonData['team_card_img'][$i].
    '"><h3>'.celanHTML($jsonData['team_card_name'][$i]).'</h3><div class="role">'.celanHTML($jsonData['team_card_title'][$i]).
    '</div><hr><a class="in" href="'.$jsonData['team_card_linkedin'][$i].'"  target="_blank" ><div class="LinkIco"><i class="fa fa-linkedin" aria-hidden="true"></i></div><p>'.celanHTML($jsonData['team_card_name'][$i]).
    '</p></a><a class="mail" href="mailto:'.$jsonData['team_card_email'][$i].'"><div class="LinkIco"><span class="glyphicon glyphicon-envelope"></span></div><p>'.$jsonData['team_card_email'][$i].'</p></a><div class="link bio" data-toggle="modal" data-target="#cardModalId'.$i.'">Click For Bio</div></div>';
  }
}
?></div><div class="form press"><div data-aos="zoom-in" class="Ftitle">Press Release
</div>
<div data-aos="fade-up" class="dataText"><?php
if (isset($jsonData['press_section_data'])){
  for ($i =0; $i < count($jsonData['press_section_data']);$i++){
    echo "<p>".celanHTML($jsonData['press_section_data'][$i])."</p><p><a href='".$jsonData['press_section_url'][$i]."' target='_blank'><i>Read more</i></a></p><br>";
  }
}
?></div></div><div class="form contact"><div id="layer"></div><div data-aos="zoom-in" class="Ftitle">CONTACT
</div><form action="javascript:sendMail();" data-aos="fade-right"><label id="description">For any general inquiries, please fill in the following contact form:
</label><div id="inputs"><input type="text" name="name" placeholder="Name"><input type="text" name="subject" placeholder="Subject"><input type="email" name="email" placeholder="E-mail"><input type="tel" name="tel" placeholder="Telephone"></div><textarea name="message" rows="4" placeholder="Message">
</textarea><button type="submit">Send
</button></form><span id="htLine"></span><div id="contactDirectly" data-aos="fade-left"><?php
if (isset($jsonData['contact_email_mail'])){
  for ($i =0; $i < count($jsonData['contact_email_mail']);$i++){
    echo "<a href='mailto:".$jsonData['contact_email_mail'][$i]."' class='linkContact mailCon'><div class='CoIco'><span class='glyphicon glyphicon-envelope'></span></div><div class='adressData'>".$jsonData['contact_email_mail'][$i]."</div></a>";
    echo "<a href='waze://?q=".$jsonData['address_text'][$i]."' class='linkContact locationCon'><div class='CoIco'><span class='glyphicon glyphicon-map-marker'></span></div><div class='adressData'>".$jsonData['address_text'][$i]."</div></a>";
    echo "<div class='map' id='map".$i."'></div>";
  }
  }
?></div></div><footer><div id="bootomTtle"><span class="glyphicon glyphicon-copyright-mark"></span> 2017-2020 YAD Capital LLC.
</div></footer><?php
if (isset($jsonData['team_card_img'])){
  for ($i =0; $i < count($jsonData['team_card_img']);$i++){
    echo "<div class='modal fade BioCard' id='cardModalId".$i."' role='dialog'>
    <div class='modal-dialog'>
      <div class='modal-content'>
        <div class='modal-header media'>
          <div class='media-left'>
            <img src='".$jsonData['team_card_img'][$i]."' class='media-object' style='width:60px' alt='".celanHTML($jsonData['team_card_name'][$i])."' >
          </div>
          <div class='media-body'>
            <h4 class='media-heading'>".celanHTML($jsonData['team_card_name'][$i])."</h4>
          </div>
          <div class='media-right'>
            <button type='button' class='close' data-dismiss='modal'>&times;</button>
          </div>
        </div>
        <div class='modal-body'>
          <p>".celanHTML($jsonData['team_card_bio'][$i])."</p>
        </div>
      </div>
    </div>
  </div>";
  }
}

?>
<!-- Modal Legal Disclaimer -->
  <div class="modal fade" id="LegalDisclaimerModal" role="dialog">
    <div class="modal-dialog">
      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header media">
          <div class="media-body">
            <h4 class="media-heading">Legal Disclaimer</h4>
          </div>
          <div class="media-right">
            <button type="button" class="close" data-dismiss="modal">&times;</button>
          </div>
        </div>
        <div class="modal-body">
          <p><?php
          echo celanHTML($jsonData['legal_disclaimer'][0]);
          ?></p>
        </div>
      </div>
    </div>
  </div>
 <script>
  function initMap() {
    var location;
    var map;
    var coordInfoWindow;
    <?php
    if (isset($jsonData['address_pointer'])){
        for ($i =0; $i < count($jsonData['team_card_img']);$i++){
        echo "location = new google.maps.LatLng(".celanHTML($jsonData['address_pointer'][$i]).");";
        echo "map = new google.maps.Map(document.getElementById('map".$i."'), {
          center: location,
          zoom: 14
        });
        coordInfoWindow = new google.maps.InfoWindow();
        coordInfoWindow.setContent('YAD Capital LLC');
        coordInfoWindow.setPosition(location);
        coordInfoWindow.open(map);";
        }
    }
    ?>
  }
</script>
<script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyC3XSPD7dNWCkDaI4JJIe3EpzvN3mhJQ5I&callback=initMap&language=en">
</script>
<!--parallax, FontAwesome, Bootstrap -->
<script src="files/Libraries.js"></script>
<!--AOS OnScroll -->
<script src="https://cdn.rawgit.com/michalsnik/aos/2.1.1/dist/aos.js"></script>
<script src="files/home.js"></script>
</body>
</html>
