<?php

date_default_timezone_set('America/New_York');

$lines = file('../db.conf');
$db = trim($lines[0]);
$user = trim($lines[1]);
$dbpw = trim($lines[2]);
$userpw = trim($lines[3]);

$conn = mysql_connect('localhost', $user, $dbpw)
or die ('I cannot connect to the database.');
mysql_select_db($db); 

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $candidate_userpw = mysql_real_escape_string($_POST['pw']);
    if ($userpw != $candidate_userpw) {
        header('HTTP/1.0 401 Unauthorized');
        echo 'incorrect password';
    } else {
        $cost = mysql_real_escape_string($_POST['cost']);
        $category = mysql_real_escape_string($_POST['category']);
        $comment = mysql_real_escape_string($_POST['comment']);
        $datetime = date('Y-m-d H:i:s');
        $query = 'INSERT INTO expense (cost, category, datetime, comment) VALUES (';
        $query .= $cost . ', "' . $category . '", "' . $datetime . '", "' . $comment . '");';
        $result = mysql_query($query);
        if (!$result) {
            die('Invalid query: ' . mysql_error());
        }
        echo 'success';
    }
}

mysql_close($conn);

?>
