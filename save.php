<?php

$lines = file('db.conf');
$db = trim($lines[0]);
$user = trim($lines[1]);
$pw = trim($lines[2]);

$dbh = mysql_connect('localhost', $user, $pw)
or die ('I cannot connect to the database.');
mysql_select_db($db); 

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $cost = mysql_real_escape_string($_POST['cost']);
    //$query = 'INSERT INTO expense (cost) VALUES ("';
    //$query .= $cost . '"';
    var_dump($cost);
    //mysql_query($query);
}

mysql_close($conn);

?>
