<!DOCTYPE html>
<html>
 <head>
  <title>ד"ר רובין השתלות שיניים</title>
	<!--HTML base-->
	<base href="https://dr-rubin.yjacob.net/">
	<!--Hebrew-->
	<meta charset="utf-8"/>
	<meta name="description" content="ד'ר יהודה רובין הוא רופא שיניים מומחה להשתלות שיניים.">
	<meta name="keywords" content="השתלות שיניים,הרמת הסינוס,עבודה עם לייזר,לייזר CO2,לייזר Diode,לייזר Erbium,Disks Implants,PRF">
	<!--Responsiv-->
	<meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0" />
	<!--css-->
  	<link rel="stylesheet" href="index.css">
	<link rel="stylesheet" href="heb.css">
	<link rel="stylesheet" type="text/css" href="fancybox/jquery.fancybox.css">
	<!--font awesome-->
	<script src="https://use.fontawesome.com/9a4307ff22.js"></script>
  	<link href="https://use.fontawesome.com/9a4307ff22.css" media="all" rel="stylesheet">
	<!--Jquery-->	
	<script type="text/javascript" src="https://code.jquery.com/jquery-latest.min.js"></script>
	<!--<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script>-->
	<!--ICON-->
	<link rel="icon" href="images/Icon.jpg" type="image/x-icon">	
	<link rel="shortcut icon" href="images/Icon.jpg" type="image/x-icon">	
	<!--AOS OnScroll-->
	<link href="https://cdn.rawgit.com/michalsnik/aos/2.1.1/dist/aos.css" rel="stylesheet">
	<!--Google reCAPTCHA-->
	<script src='https://www.google.com/recaptcha/api.js'></script>
 </head>
 <body class="activeScrool">
<?php
		if(isset($_GET['data']))
		{
			 echo '<input id="spesialLink" type="hidden" name="'.$_GET["data"].'">';
		}
?>
   <header>
     <div id="headerMaiDiv">
       <img src="images/lee_ico_320x319.jpg" alt="DrRubinIcon">
       <hr><div id="headerMaiDivText"><h1>ד"ר יהודה רובין</h1><h2>השתלות שיניים בלעדי</h2></div>
     </div>
     <div id="goDownButton"><div id="goDownText">קרא עוד</div><div id="goDownI"><i class="fa fa-chevron-down" aria-hidden="true"></i></div></div>
   </header><nav class="">
		<div id="lan">
			<a id="defult"><img src="images/Israel_flag.png" alt="English"></a><br>
			<div id="moreLan">
				<a href="English"><img src="images/USA_flag.png" alt="Hebrew"></a><br>
				<a href="French"><img src="images/Franch_flag.png" alt="French"></a><br>
			</div>
		</div>
		 <div id="barlink">
			<a class="About">אודות</a>
			<a class="Certificates">תעודות</a>
			<a class="Contact">צור קשר</a>
		</div>
	 </nav><div id="body">
   <div id="about" class="form">
		 <div class="title">אודות</div>
		 <img id="leeimg" src="images/leeimg.jpg" data-aos="fade-up" alt="Dr Rubin IMG">
		 <input id="GetToHear" type="hidden" value="Laser">
		 <p>בס"ד<br>
ד"ר יהודה לי- דוד רובין, נולד ב 1969 בצרפת.
<br>Universite Paris VII, faculte La Garanciere ב- 1996 סיים את לימודיו ברפואת השיניים ב 
<br>ב1998 הגיש את התזה שלו על ניתוחי חניכיים וקיבל את הדוקטורט ברפואת השיניים. הוא התקדם בלימודיו לפוסט דוקטורט והתמחה בהשתלות שיניים. הוא ביצע השתלות שיניים בבית החולים שע"י האוניברסיטה של  Lille (France) ובמקביל עבד כרופא שיניים במספר מרפאות שיניים פרטיות.
<br>בשנת 2000 ד"ר רובין עלה לארץ עבר בהצלחה את מבחני משרד הבריאות בישראל וקיבל את רישיון רפואת השיניים מטעמם.
<br>ד"ר רובין עבר סידרה של השתלמויות בארץ ובארה"ב בהשתלות עצם, בהרמת סינוס ובניתוחי חניכיים לכיסוי שורשים (במקרה של נסיגת חניכיים) ע"מ לתת למטופליו איכות מקצועית בלתי מתפשרת ולהעניק להם את ההזדמנות לחיוך אסתטי.
<br>משנת 2002 ד"ר רובין החל להשתמש בשיטה החדשנית של השתלה בלייזר. טכניקה משודרגת  המונעת כירורגיה ע"י סכין ותפרים.
<br><br>ד"ר רובין מתעדכן ומתמקצע 'און ליין' בשיטות חדשניות ובטכניקות מתקדמות, מוכרות ופחות ידועות בארץ ובעולם במגוון רחב של תחומי רפואת השיניים כמו:
<br>-<strong> העמסה מיידית</strong>: הכוללת עקירת שיניים, שתלים, וכתרים זמניים באותה פגישה! אפילו בפה שלם!
<br>-<strong title="לייזר CO2"> לייזר CO2</strong>: לטיפול ברקמה הרכה של הפה.
<br>-<strong title="לייזר Diode"> לייזר diode</strong>: להשתלות ולהלבנת שיניים.
<br>-<strong title="לייזר Erbium"> לייזר erbium</strong>: לטיפול בעצם/בשן.
<br>-<strong> Lumineers</strong>: לשיפור המראה האסתטי- ציפוי "חרסינה" דק כעדשת מגע המוצמד לחזית השן ללא הרדמה ולעיתים אף ללא השחזת השן.
<br>-<strong title="PRF"> שימוש ב A –PRF</strong>: עידוד צמיחת חניכיים ועצם ע"י שימוש בדם המטופל.
<br>-<strong> השתלות מתוכננות דרך המחשב</strong>: טכנולוגיה המונעת סיכון פגיעה בעצב.
<br>-<strong title="הרמת סינוס"> טכניקות מתקדמות להרמת סינוס בתהליך מהיר</strong>: (, maxillent's  i-raise בלון)
<br>-<strong title="Disk Implant"> Disk implant</strong>: שתלים המותאמים למקרים בהם אין מספיק גובה בעצם הלסת והמטופל לא מעוניין בהשתלת עצם.
<br><br><br>בשנת 2010 ד"ר רובין זכה בתואר:
<br>"FELLOW OF ORAL IMPLANTOLOGY  from the Word Congress of implantologists"
<br><br> לאחר כ 20 שנות ניסיון אנו מזמינים אתכם למרפאותינו בירושלים ובתל אביב. אנו מקווים שנזכה להיות עבורכם שליחים נאמנים ולהעניק לכם כמו לכל מטופלינו את הטיפול המיטבי והמרבי, במקצועיות, באמינות ובמסירות.
<br>ובהתאמה ל"אני מאמין שלי": "אין עוד מלבדו, בשם ד' נעשה ונצליח"
		 </p>
	 </div><div id="certificates" class="form">
	<div class="title">תעודות</div>
	 <div  id="imgContainer">
	<a href="Certificates/img6.jpg" data-fancybox="group" data-caption="ד''ר רובין - תעודות והערכות">
		<img src="Certificates/img6s.jpg" alt="CertificatesImg" />
	</a>
	<a href="Certificates/img2.jpg" data-fancybox="group" data-caption="ד''ר רובין - תעודות והערכות">
		<img src="Certificates/img2s.jpg" alt="CertificatesImg" />
	</a>
	<a href="Certificates/img7.jpg" data-fancybox="group" data-caption="ד''ר רובין - תעודות והערכות">
		<img src="Certificates/img7s.jpg" alt="CertificatesImg" />
	</a>
	<a href="Certificates/img1.jpg" data-fancybox="group" data-caption="ד''ר רובין - תעודות והערכות">
		<img src="Certificates/img1s.jpg" alt="CertificatesImg" />
	</a>
	<a href="Certificates/img3.jpg" data-fancybox="group" data-caption="ד''ר רובין - תעודות והערכות">
		<img src="Certificates/img3s.jpg" alt="CertificatesImg" />
	</a>
	<a href="Certificates/img4.jpg" data-fancybox="group" data-caption="ד''ר רובין - תעודות והערכות">
		<img src="Certificates/img4s.jpg" alt="CertificatesImg" />
	</a>
	<a href="Certificates/img8.jpg" data-fancybox="group" data-caption="ד''ר רובין - תעודות והערכות">
		<img src="Certificates/img8s.jpg" alt="CertificatesImg" />
	</a>
	<a href="Certificates/img9.jpg" data-fancybox="group" data-caption="ד''ר רובין - תעודות והערכות">
		<img src="Certificates/img9s.jpg" alt="CertificatesImg" />
	</a>
	<a href="Certificates/img10.jpg" data-fancybox="group" data-caption="ד''ר רובין - תעודות והערכות">
		<img src="Certificates/img10s.jpg" alt="CertificatesImg" />
	</a>
	<a href="Certificates/img5.jpg" data-fancybox="group" data-caption="ד''ר רובין - תעודות והערכות">
		<img src="Certificates/img5s.jpg" alt="CertificatesImg" />
	</a>
	 </div>
	 </div><div id="contact" class="form">
		<div class="title">צור קשר</div>
	 <form action="message.php" method="post">		 
		 <input type="text" name="fullName" placeholder="שם מלא">
		 <input type="text" name="topic" placeholder="נושא הודעה">
		 <input type="tel" name="tel" placeholder="מספר טלפון">
		 <input type="email" name="email" placeholder="כתובת אימייל">
		 <textarea name="details" cols="30" rows="5" placeholder="ההודעה שלך"></textarea>
		 <div id="GoogleCheck" class="g-recaptcha" data-sitekey="6LdTOBgUAAAAABnQOnadEQ_dODCP6KrQfhi2FGxv"></div>
		 <input type="button" onclick="SendMessage()" value="שלח">
	 </form>
	 <div class="ORline"><hr>או<hr></div>
	 <div id="contactDirect">
	 <a id="mailtoA" href="mailto:yld.rubin@gmail.com?subject=New_Client"><i class="fa fa-envelope-o" aria-hidden="true"></i><hr>yld.rubin@gmail.com
	 </a><a id="tellA" href="tel:+972-50-828-3507"><i class="fa fa-phone" aria-hidden="true"></i><hr>050-828-3507
	 </a><a id="smsA"  href="sms:+972-50-828-3507"><i class="fa fa-commenting-o" aria-hidden="true"></i><hr>050-828-3507
	</a><a id="facebook"  href="https://www.facebook.com/DrYehudaRubin"><i class="fa fa-facebook-square fa-2"></i><hr>facebook.com/DrYehudaRubin
	</a><a id="google"  href="https://plus.google.com/u/0/112246134280765266912/posts"><i class="fa fa-google-plus" aria-hidden="true"></i><hr>ד"ר רובין מרפאת שיניים</a>
	 </div><div class="ORline"><hr>או<hr></div>
	 <div id="placeTitle"><strong>בוא לבקר אותנו</strong>
		דוד המלך 1 תל אביב		 
		<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3380.5905305529095!2d34.781821!3d32.08032199999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x151d4b858525f5d9%3A0x34a118bfa2bb7bdf!2z157XqdeR16bXqg!5e0!3m2!1siw!2sil!4v1432542306425" ></iframe>
	 </div>
	 </div></div><footer><div id="copyright"><i class="fa fa-copyright" aria-hidden="true"></i><a href="http://all-in-one.cf">All In One</a></div>
	 <div id="bottomLinks">Titles: <a href="Hebrew/לייזר CO2">לייזר CO2</a><a href="Hebrew/לייזר Diode">לייזר Diode</a><a href="Hebrew/לייזר Erbium">לייזר Erbium</a><a href="Hebrew/הרמת סינוס">הרמת סינוס</a><a href="Hebrew/PRF">PRF</a><a href="Hebrew/Disk Implant">Disk Implant</a></div>
	 </footer>
	<!--AOS OnScroll-->
   	<script src="https://cdn.rawgit.com/michalsnik/aos/2.1.1/dist/aos.js"></script>
   	<!--Fancybox-->
	<script src="fancybox/jquery.fancybox.min.js"></script>
   	<script type="text/javascript" src="index.js"></script>   
	 <!--google Analytics-->
	<script>
	  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
	  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
	  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
	  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

	  ga('create', 'UA-58141423-1', 'auto');
	  ga('send', 'pageview');
	</script>
	<script type="text/javascript">
	/*AOS OnScroll (JS)*/
	AOS.init({
		duration: 1200,
	});
	</script>
</body>
	
</html>