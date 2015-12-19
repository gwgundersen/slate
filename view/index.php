<!DOCTYPE HTML PUBLIC=''>
<html>
<?php include 'header.php'; ?>
<body>
    <div class='container'>
        <h1>Report</h1>
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
        
        $candidate_userpw = $_POST['pw'];
        if ($userpw != $candidate_userpw) {
            header('HTTP/1.0 401 Unauthorized');
            echo 'incorrect password';
        } else {
            $query = 'SELECT amount FROM surplus;';
            $result = mysql_query($query);
            $amount = floatval(mysql_fetch_array($result)[0]);
            $query = 'SELECT SUM(cost) FROM expense;';
            $result = mysql_query($query);
            $spent = floatval(mysql_fetch_array($result)[0]);
            $delta = $amount - $spent;

            $output = '<div>';
            $output .= '<a href="/slate">Back</a>';
            $output .= '<p class="highlight">' . $delta .'</p>';
            $output .= '</div>';

            $query = 'SELECT * FROM expense;';
            $result = mysql_query($query);
            if (!$result) {
                die('Invalid query: ' . mysql_error());
            }
            $output .= '<table class="table">';
            $output .= '<thead><tr><td>Date</td><td>Cost</td><td>Category</td><td>Comment</td></tr></thead>';
            while($row = mysql_fetch_array($result)) {
                $output .= '<tr>';
                $output .= '<td>' . date('M j', strtotime($row['datetime'])) . '</td>';
                $output .= '<td>' . $row['cost'] . '</td>';
                $output .= '<td>' . $row['category'] . '</td>';
                $output .= '<td>' . $row['comment'] . '</td>';
                $output .= '</tr>';
            }
            $output .= '</table>';
            echo $output;
        }
    }

    mysql_close($conn);

    ?>
    </div>
</body>
</html>
