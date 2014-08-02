function funcDelete(deleteId) {
	var $r = confirm("Are you sure?");
	var $url = 'slate.php?func=delete&id=' + deleteId;
	if ($r == true) {
		$.ajax({
			url: $url,
			type: 'GET',
			success: function(resp) {
				console.log("Success!");
			}
		});
	}
	$('#expenses-table tbody').load('slate.php?func=view');
}
$(document).ready(function() {

	// variables
	var dateToggle 	= 3; // because this loads by default, the first click should make the number even
	var costToggle 	= 2;
	var categoryToggle = 2;
	
	// view and view functions
	$('#view-button').click(function(e) {
		e.preventDefault();
		$('#submit-form').slideUp();
		$('#view-form').slideUp();
		$('#view-panel').slideDown('slow');
		$('#hr-main').hide('slow');
		$('#expenses-table tbody').load('slate.php?func=view');
	});
	
	// more details
	$('#expenses-table').on('click', '.button-more', function(e) {
		e.preventDefault();
		var $currentId = $(this).attr('id');
		$('#details1-' + $currentId).load('slate.php?func=details1&id=' + $currentId, function() {
			$('#details1-' + $currentId).slideDown(500);
		});
		$('#details2-' + $currentId).load('slate.php?func=details2&id=' + $currentId, function() {
			$('#details2-' + $currentId).slideDown(500);
		});
		$('#more-less-placeholder-' + $currentId).load('slate.php?func=more&id=' + $currentId);
	});
	
	// less details
	$('#expenses-table').on('click', '.button-less', function(e) {
		e.preventDefault();
		var $currentId = $(this).attr('id');
		$('#details1-' + $currentId).slideUp(500);
		$('#details2-' + $currentId).slideUp(500);
		$('#' + $currentId).slideUp(500);
		$('#more-less-placeholder-' + $currentId).load('slate.php?func=less&id=' + $currentId);
	});
	$('#back-button').click(function(e) {
		e.preventDefault();
		$('#view-panel').slideUp(300);
		$('#submit-form').slideDown();
		$('#view-form').slideDown();
		$('#hr-main').show('slow');
	});
	
	// sort by
	$('#sort-by-date').click( function(e) {
		e.preventDefault();
		if (dateToggle % 2 == 0) {
			$('#expenses-table tbody').load('slate.php?func=view&sortby=date');
		}
		else {
			$('#expenses-table tbody').load('slate.php?func=view&sortby=date&order=desc');
		}
		dateToggle++;
	});
	$('#sort-by-cost').click( function(e) {
		e.preventDefault();
		if (costToggle % 2 == 0) {
			$('#expenses-table tbody').load('slate.php?func=view&sortby=cost');
		}
		else {
			$('#expenses-table tbody').load('slate.php?func=view&sortby=cost&order=desc');
		}
		costToggle++;
	});
	$('#sort-by-category').click( function(e) {
		e.preventDefault();
		if (categoryToggle % 2 == 0) {
			$('#expenses-table tbody').load('slate.php?func=view&sortby=category');
		}
		else {
			$('#expenses-table tbody').load('slate.php?func=view&sortby=category&order=desc');
		}
		categoryToggle++;
	});
	
	// ajax submission
	$("#submit-button").click(function(e) {
	
		// get form data
		var numRegex 	= /^[+-]?\d+(\.\d+)?([eE][+-]?\d+)?$/;
		var varCostTemp = $('#cost').val();
		var varCategory = $('#category').val();
		var varComment  = $('#comment').val();
		e.preventDefault();
		
		// errors
		if (varCostTemp == false && varCategory == "select") {
			alert("Please input a cost and select a category.");
		}
		else if ((varCostTemp && numRegex.test(varCostTemp) == false) && varCategory == "select") {
			alert("Please use only numbers (no symbols).");
		}
		else if (varCategory == "select") {
			alert("Please select a category.");
		}
		else if (varCostTemp == false) {
			alert("Please input a cost.");
		}
		else if (varCostTemp && numRegex.test(varCostTemp) == false) {
			alert("Please use only numbers (no symbols).");
		}
		
		// fire slate.php
		else {
			var varCost = varCostTemp;
			$.ajax({
				url: 'slate.php',
				type: 'POST',
				dataType: 'html',
				data: {
					cost: varCostTemp,
					category: varCategory,
					comment: varComment
				},
				success: function(resp) {
					alert("Success!");
					window.location.reload();
				},
				error: function(xhr, status, message) {
					alert("There was an error: " + message);
				}
			});
		}
	});
});