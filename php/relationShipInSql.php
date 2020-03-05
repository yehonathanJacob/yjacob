<?php 
$conn->query('SELECT u.ID, i.KName, u.Name, u.Pic, u.Detalis, u.Price 
	FROM Prodocts u LEFT JOIN Katalogs i 
	ON (i.ID = u.KatalId)');
 ?>