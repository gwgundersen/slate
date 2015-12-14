<?php

// Variables
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

mysql_close($conn);
?>
