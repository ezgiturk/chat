/* if the page has been fully loaded we add two click handlers to the button */
$(document).ready(function () {
	/* Get the checkboxes values based on the class attached to each check box */
	$("#buttonClass").click(function() {
	    getValueUsingClass();
	});
	
	/* Get the checkboxes values based on the parent div id */
	$("#buttonParent").click(function() {
	    getValueUsingParentTag();
	});
});

function getValueUsingClass(){
	/* declare an checkbox array */
	var chkArray = [];
	
	/* look for all checkboes that have a class 'chk' attached to it and check if it was checked */
	$(".chk:checked").each(function() {
		chkArray.push($(this).val());
	});
	
	/* we join the array separated by the comma */
	var selected;
	selected = chkArray.join(',') ;
	
	/* check if there is selected checkboxes, by default the length is 1 as it contains one single comma */
	if(selected.length > 0){
		alert("You have selected " + selected);	
	}else{
		alert("Please at least check one of the checkbox");	
	}
}

function getValueUsingParentTag(){
	var chkArray = [];
	
	/* look for all checkboes that have a parent id called 'checkboxlist' attached to it and check if it was checked */
	$("#checkboxlist input:checked").each(function() {
		chkArray.push($(this).val());
	});
	
	/* we join the array separated by the comma */
	var selected;
	selected = chkArray.join(',') ;
	
	/* check if there is selected checkboxes, by default the length is 1 as it contains one single comma */
	if(selected.length > 0){
		alert("You have selected " + selected);	
	}else{
		alert("Please at least check one of the checkbox");	
	}
}