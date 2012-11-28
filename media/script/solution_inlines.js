// checker_results_inline.html
$(document).ready(function(){
	$("h3.clickable").css('cursor', 'pointer').click(function(){
		$(this).next("div").slideToggle("fast");
		$(this).children("a").children("span").toggleClass("ui-icon-triangle-1-s").toggleClass("ui-icon-triangle-1-e");
	}).click();
	//Stop the link click from doing its normal thing
	return false;
});


// solution_files_inline.html
$(function() { // perform JavaScript after the document is scriptable. 
	// setup ul.tabs to work as tabs for each div directly under div.panes 
	$(".file>h3").remove();
	$(".filetabs").tabs();
}); 
