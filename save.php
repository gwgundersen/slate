<?php

// Variables
//$func	= $_GET['func'];
//$sortby	= $_GET['sortby'];
//$order	= $_GET['order'];
//$getID	= $_GET['id'];

// submit
// for error submission error messages, see /js/slate.js
/*if ($_POST['category'] && $_POST['cost']) {
	
	$cost 	  = $_POST['cost'];
	$category = $_POST['category'];
	$comment  = $_POST['comment'];

	$query = 'INSERT INTO Purchases (budget_cost, budget_category, budget_comment) VALUES ('';
	$query .= $cost . '','';
	$query .= $category . '','';
	$query .= $comment . '')';
	mysql_query($query);
}*/

$lines = file('db.conf');
$db = $lines[0];
$user = $lines[1];
$pw = $lines[2];

$dbh = mysql_connect('localhost', $user, $pw)
or die ('I cannot connect to the database.');
mysql_select_db($db); 

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    var_dump($_POST['cost']);
    $query = 'INSERT INTO expense (cost) VALUES ("';
    $query .= $cost . '"';
    echo($query);
    mysql_query($query);
}

mysql_close($conn);
?>
