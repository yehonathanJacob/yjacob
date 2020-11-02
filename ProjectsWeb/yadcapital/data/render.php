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
  <link rel="stylesheet" href="files/home.css?v=2.0">
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
?><!--
David Perez Card
--><!-- <div id="davidPerez" data-aos="flip-right" class="card">
<img class="profilePic" src="images/DavidPerez.jpg" alt="David Perez profile"><h3>
David Perez</h3><div class="role">Co-Founding Partner
</div><hr><a class="in" href="https://www.linkedin.com/in/david-perez-a65b04124/" target="_blank" ><div class="LinkIco"><i class="fa fa-linkedin" aria-hidden="true"></i></div><p>David Perez</p>
</a><a class="mail" href="mailto:david@yadcapital.com"><div class="LinkIco"><span class="glyphicon glyphicon-envelope"></span></div><p>david@yadcapital.com</p>
</a><div id="davidPerezBio" class="link bio" data-toggle="modal" data-target="#DavidPerezModal">Click For Bio</div>
</div> --><!--
Daniel Rubin Card
--><!-- <div id="danielRubin" data-aos="flip-right" class="card">
<img class="profilePic" src="images/danielRubin.jpg" alt="Daniel Rubin profile"><h3>Daniel Rubin
</h3><div class="role">Co-Founding Partner
</div><hr><a class="in" href="https://www.linkedin.com/in/daniel-rubin/" target="_blank" ><div class="LinkIco"><i class="fa fa-linkedin" aria-hidden="true"></i></div><p>Daniel Rubin</p>
</a><a class="mail" href="mailto:daniel@yadcapital.com"><div class="LinkIco"><span class="glyphicon glyphicon-envelope"></span></div><p>daniel@yadcapital.com</p>
</a><div id="danielRubinBio" class="link bio" data-toggle="modal" data-target="#DanielRubinModal">Click For Bio</div>
</div> --></div><div class="form press"><div data-aos="zoom-in" class="Ftitle">Press Release
</div>
<div data-aos="fade-up" class="dataText"><?php
if (isset($jsonData['press_section_data'])){
  for ($i =0; $i < count($jsonData['press_section_data']);$i++){
    echo "<p>".celanHTML($jsonData['press_section_data'][$i])."</p><p><a href='".$jsonData['press_section_url'][$i]."' target='_blank'><i>Read more</i></a></p><br>";
  }
}
?>
  <!-- <p>
  <i>December 19, 2019</i>
  </p>
  <p>
  <i><strong>YAD Capital and Realio join forces to raise a $5 million tokenized fund</strong></i>
  </p>
  <p>Realio will issue a $5 million tokenized fund via the Reg D 506 (c) and Reg S exemptions, enabling global participation in a niche investment product normally reserved for a select subset of institutional investors.</p>
  <p><a href="https://www.prnewswire.com/news-releases/realio-and-yad-capital-join-forces-to-raise-a-5-million-tokenized-fund-on-fusion-blockchain-300977876.html?tc=eml_cleartime" target="_blank"><i>Read more</i></a></p>
  <p><br>
  <i>September 26, 2019</i>
  </p>
  <p>
  <i><strong>YAD Capital partners with Fusion Foundation to bring its alternative credit portfolio onto Fusion’s cryptofinance ecosystem</strong></i>
  </p>
  <p>The fractionalization of assets enabled by blockchain will bring transparency in the merchant cash advance industry and broaden our global reach to investors.</p>
  <p><a href="https://bit.ly/2m7rCZd" target="_blank"><i>Read more</i></a></p> -->
</div></div><div class="form contact"><div id="layer"></div><div data-aos="zoom-in" class="Ftitle">CONTACT
</div><form action="javascript:sendMail();" data-aos="fade-right"><label id="description">For any general inquiries, please fill in the following contact form:
</label><div id="inputs"><input type="text" name="name" placeholder="Name"><input type="text" name="subject" placeholder="Subject"><input type="email" name="email" placeholder="E-mail"><input type="tel" name="tel" placeholder="Telephone"></div><textarea name="message" rows="4" placeholder="Message">
</textarea><button type="submit">Send
</button></form><span id="htLine"></span><div id="contactDirectly" data-aos="fade-left"><?php
if (isset($jsonData['contact_email_mail'])){
  for ($i =0; $i < count($jsonData['contact_email_mail']);$i++){
    echo "<a href='mailto:".$jsonData['contact_email_mail'][$i]."' class='linkContact mailCon'><div class='CoIco'><span class='glyphicon glyphicon-envelope'></span></div><div class='adressData'>".$jsonData['contact_email_mail'][$i]."</div></a>";
  }
}
?><!-- <a href="mailto:david@yadcapital.com" class="linkContact mailCon"><div class="CoIco"><span class="glyphicon glyphicon-envelope"></span></div><div class="adressData">david@yadcapital.com</div></a> --><!-- <a href="mailto:daniel@yadcapital.com" class="linkContact mailCon"><div class="CoIco"><span class="glyphicon glyphicon-envelope"></span></div><div class="adressData">daniel@yadcapital.com</div></a> --><?php
if (isset($jsonData['address_text'])){
  for ($i =0; $i < count($jsonData['address_text']);$i++){
    echo "<a href='waze://?q=".$jsonData['address_text'][$i]."' class='linkContact locationCon'><div class='CoIco'><span class='glyphicon glyphicon-map-marker'></span></div><div class='adressData'>".$jsonData['address_text'][$i]."</div></a>";
  }
}
?><!-- <a href="waze://?q=590 Madison Avenue New York, NY 10022" class="linkContact locationCon"><div class="CoIco"><span class="glyphicon glyphicon-map-marker"></span></div><div class="adressData">1345 Avenue of the Americas, 33rd floor New York, NY 10105 </div></a> --><div id="map"></div></div></div><footer><div id="bootomTtle"><span class="glyphicon glyphicon-copyright-mark"></span> 2017-2019 YAD Capital LLC.
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
<!-- Modal Daniel Rubin Card -->
  <!-- <div class="modal fade BioCard" id="DanielRubinModal" role="dialog">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header media">
          <div class="media-left">
            <img src="images/danielRubin.jpg" class="media-object" style="width:60px" alt="Daniel Rubin profile">
          </div>
          <div class="media-body">
            <h4 class="media-heading">Daniel Rubin</h4>
          </div>
          <div class="media-right">
            <button type="button" class="close" data-dismiss="modal">&times;</button>
          </div>
        </div>
        <div class="modal-body">
          <p>Mr. Daniel Rubin has over 19 years of principal investing, investment banking, restructuring and operational experience, primarily in the real estate industry.
<br>
Prior to co-founding YAD Capital LLC, Mr. Rubin was the COO &amp; CFO of Halpern Real Estate Ventures LLC where he assumed a strategic role in the overall management of the firm and was responsible for executing and managing over $650 million of real estate transactions.
<br>
Prior to that, Mr. Rubin invested in and advised several real estate operating companies, REITs and private equity real estate firms on more than $4.5 billion of complex corporate finance transactions at various organizations including Silverkey Capital, JEN Partners, Lehman Brothers and EdgeRock Realty Advisors. Mr. Rubin started his career at Deloitte, first as an auditor and subsequently as a turnaround consultant.
<br>
Mr. Rubin holds an MBA from NYU Stern School of Business, an M.S. degree in Financial Engineering from University of Paris Creteil, and a B.S. degree in Accounting, Finance, and Corporate Taxation from University of Paris Dauphine. Mr. Rubin is a member of the NYU Stern School of Business Alumni Council and Chair of its Finance Committee.</p>
        </div>
      </div>
    </div>
  </div> -->
 <!-- Modal David Perez Card -->
  <!-- <div class="modal fade BioCard" id="DavidPerezModal" role="dialog">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header media">
          <div class="media-left">
            <img src="images/DavidPerez.jpg" class="media-object" style="width:60px" alt="David Perez profile">
          </div>
          <div class="media-body">
            <h4 class="media-heading">David Perez</h4>
          </div>
          <div class="media-right">
            <button type="button" class="close" data-dismiss="modal">&times;</button>
          </div>
        </div>
        <div class="modal-body">
          <p>Mr. David Perez has over 18 years of trading and investment experience in liquid macro assets.
<br>
Prior to co-founding YAD Capital LLC, Mr. Perez was a senior Portfolio Manager and Managing Director at MKP Capital Management LLC, a $7 billion diversified alternative asset manager focused on macro and credit opportunities, where he was managing a $500 million portfolio of stocks, bonds, credit and currencies.
<br>
Prior to that, Mr. Perez was a Managing Director at Goldman Sachs, where he spent 14 years, most recently as the Head of its US Index Volatility Trading Business. He spent the first 6 years in London, and the last 8 years in New York.
<br>
Mr. Perez studied in Paris, France where he received a B.A. in Computer Sciences and Mathematics from University Paris Dauphine, as well as an M.S. degree in Finance.</p>
        </div>
      </div>
    </div>
  </div> -->
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
    var location = new google.maps.LatLng(<?php echo celanHTML($jsonData['address_pointer'][0]); ?>);

    var map = new google.maps.Map(document.getElementById('map'), {
      center: location,
      zoom: 14
    });
    var coordInfoWindow = new google.maps.InfoWindow();
    coordInfoWindow.setContent('YAD Capital LLC');
    coordInfoWindow.setPosition(location);
    coordInfoWindow.open(map);
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
