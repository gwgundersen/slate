<!DOCTYPE HTML PUBLIC=''>
<html>
<body>
    <?php

    date_default_timezone_set('America/New_York');

    $lines = file(dirname(__FILE__) . '/../db.conf');
    $db = trim($lines[0]);
    $user = trim($lines[1]);
    $dbpw = trim($lines[2]);
    $userpw = trim($lines[3]);

    $conn = mysql_connect('localhost', $user, $dbpw)
    or die ('I cannot connect to the database.');
    mysql_select_db($db); 

    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
        
        $candidate_userpw = $_GET['pw'];
        # There is nothing truly secure about this. Someone would have to care enough.
        if ($userpw != $candidate_userpw) {
            echo 'incorrect password';
        } else {
            $query = 'SELECT amount FROM surplus;';
            $result = mysql_query($query);
            $amount = floatval(mysql_fetch_array($result)[0]);
            $query = 'SELECT SUM(cost) FROM expense;';
            $result = mysql_query($query);
            $spent = floatval(mysql_fetch_array($result)[0]);
            $delta = $amount - $spent;

            $output .= '<div>';
            $output .= '<a href="/slate">Back</a>';
            $output .= '<p class="highlight">' . $delta .'</p>';
            $output .= '</div>';

            $query = 'SELECT * FROM expense;';
            $result = mysql_query($query);
            if (!$result) {
                die('Invalid query: ' . mysql_error());
            }
            $output .= '<div class="table-responsive"><table class="table">';
            $output .= '<thead><tr><td>Date</td><td>Cost</td><td>Category</td><td>Comment</td></tr></thead>';
            while($row = mysql_fetch_array($result)) {
                $output .= '<tr>';
                $output .= '<td>' . date('M j', strtotime($row['datetime'])) . '</td>';
                $output .= '<td>' . $row['cost'] . '</td>';
                $output .= '<td>' . $row['category'] . '</td>';
                $output .= '<td>' . $row['comment'] . '</td>';
                $output .= '</tr>';
            }
            $output .= '</table></div>';
            echo $output;
        }
    }

    mysql_close($conn);

    ?>
</body>
</html>
