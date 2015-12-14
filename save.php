<?php
include 'global.php';

//variables
$func	= $_GET["func"];
$sortby	= $_GET["sortby"];
$order	= $_GET["order"];
$getID	= $_GET["id"];

// submit
// for error submission error messages, see /js/slate.js
if ($_POST["category"] && $_POST["cost"]) {
	
	$cost 	  = $_POST["cost"];
	$category = $_POST["category"];
	$comment  = $_POST["comment"];

	$query = "INSERT INTO Purchases (budget_cost, budget_category, budget_comment) VALUES ('";
	$query .= $cost . "','";
	$query .= $category . "','";
	$query .= $comment . "')";
	mysql_query($query);
}

// view
if ($func == "view") {

	// toggle list by date, cost, category
	$query = "SELECT budget_date, budget_cost, budget_category, budget_comment, budget_id FROM Purchases";
	if ($func == "view" && $sortby == "cost" && $order == "desc") {
		$query .= " ORDER BY budget_cost DESC";
	}
	else if ($func == "view" && $sortby == "cost") {
		$query .= " ORDER BY budget_cost";
	}
	else if ($func == "view" && $sortby == "category" && $order == "desc") {
		$query .= " ORDER BY budget_category DESC";
	}
	else if ($func == "view" && $sortby == "category") {
		$query .= " ORDER BY budget_category";
	}
	else if ($func == "view" && $sortby == "date" && $order == "desc") {
		$query .= " ORDER BY budget_date DESC";
	}
	else {
		$query .= " ORDER BY budget_date";
	}
	$result = mysql_query($query);
	$output = '';

	// view results
	while($row = mysql_fetch_assoc($result)) {
	
		// general
		$output .= "<tr>";
		$output .= "<td>" . date('M j', strtotime($row["budget_date"])) . "</td>";
		$output .= "<td class='cost-cells'>" . $row["budget_cost"] . "</td>";
		$output .= "<td>" . ucwords($row["budget_category"]) . "</td>";

		// more-less buttons
		$output .= "<td id='more-less-placeholder-" . $row["budget_id"] . "'>";
		$output .= "<a href='' class='button-more' id='" . $row["budget_id"] . "'>";
		$output .= "<img src='/images/button-more.png' class='button-toggle' /></a></td>";
		$output .= "</tr>";
		
		// placeholder cells
		$output .= "<tr id='details0-" . $row["budget_id"] . "' class='details'></tr>";		
		$output .= "<tr id='details1-" . $row["budget_id"] . "' class='details'></tr>";
		$output .= "<tr id='details2-" . $row["budget_id"] . "' class='details'></tr>";
	}
	$output .= "<tr class='table-space-2'><td><td></tr>";
	
	// view subtotals
	$query = "SELECT budget_category, SUM(budget_cost) FROM Purchases GROUP BY budget_category"; 
	$result = mysql_query($query);
	while($row = mysql_fetch_array($result)){
		$output .= "<tr><td><em>" . ucwords($row['budget_category']) . "</em></td><td class='cost-cells'>" . $row['SUM(budget_cost)'] . "</td></tr>";
	}	
	// view total
	$query = "SELECT SUM(budget_cost) FROM Purchases"; 
	$result = mysql_query($query);
	while($row = mysql_fetch_array($result)){
		$output .= "<tr class='total-cell table-space-1'><td>Total</td><td class='cost-cells'>$" . $row["SUM(budget_cost)"] . "</td></tr>";
	}
	echo $output;
}

// details0 - horizontal line
//if ($func == "details0" && $getID != null) {
	//$output = "<td colspan='3' class='hr'></td>";
	//echo $output;
//}

// details1 - comment
if ($func == "details1" && $getID != null) {
	$id = $getID;
	$query = "SELECT budget_comment FROM Purchases WHERE budget_id = " . $id;
	$result = mysql_query($query);	
	// display details
	while($row = mysql_fetch_assoc($result)) {
		$output .= "<td colspan='4'><em>Comment:</em> " . $row["budget_comment"] . "</td>";
	}
	echo $output;
}

// details2 - delete button
if ($func == "details2" && $getID != null) {
	$id = $_GET["id"];
	$query = "SELECT budget_id, budget_date, budget_cost, budget_category FROM Purchases WHERE budget_id = " . $id;
	$result = mysql_query($query);	
	while($row = mysql_fetch_assoc($result)) {
		$output .= "<td><button class='button button-delete' onclick='funcDelete(" . $row["budget_id"] . ")'>Delete</button></td>";
	}
	echo $output;
}

// details3 - more button
if ($func == "more" && $getID != null) {
	$id = $getID;
	$query = "SELECT budget_comment FROM Purchases WHERE budget_id = " . $id;
	$result = mysql_query($query);	
	// display details
	while($row = mysql_fetch_assoc($result)) {
		$output .= "<a href=''><img src='/images/button-less.png' class='button-less' id='" . $id . "'/></a>";
	}
	echo $output;
}

// details4 - less button
if ($func == "less" && $getID != null) {
	$id = $getID;
	$output = "<a href='' class='button-more' id='" . $id . "'>";
	$output .= "<img src='/images/button-more.png' class='button-toggle' /></a>";
	echo $output;
}

// delete function
if ($func == "delete" && $getID != null) {
	$id = $getID;
	$query = "DELETE FROM Purchases WHERE budget_id = " . $id;
	mysql_query($query);
	echo $output;
}

// graph
if ($func == "graph") {
	$query = "SELECT budget_cost FROM Purchases ORDER BY budget_date";
	$result = mysql_query($query);
	$dbArray = array();
	$i = 0;
	while($row = mysql_fetch_assoc($result)) {
		$dbArray[$i] = $row["budget_cost"];
		$i++;
	}
	$output = $dbArray;
	echo $output;
}

mysql_close($conn);
?>