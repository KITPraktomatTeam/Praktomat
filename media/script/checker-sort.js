// rearange the checker and make them sortable

$(document).ready(function(){
	// hide all checkergroups
	$(".inline-group.checker").hide();
	// create new a group for ALL checkers
	$("#htmlinjector_set-group").after("<div class='inline-group checker-group'><h2>Checker</h2></div>");
	var addrows = $(".inline-group.checker .add-row");
	// move the links to create new checkers
	$(".checker-group").append(addrows);
	addrows.find("a").click(function(){
		// after creation of a new checker (django js fires first) put them in the right spot (end of checkerlist) and update the ordering numbers (for the new one)
		getChecker();
		updateOrder();
	})
	// get the initial checkers
	getChecker();
	// sort them 
	$(".checker-group div").tsort("input[id$=order]", {attr:'value'});
	// apply sortebility
	$(".checker-group").sortable({
        items: 'div.inline-related',
        handle: 'h3:first',
		revert: true,
        update: function() { updateOrder(); }
    });
});

function getChecker() {
	// move checker instances in the new group before the add links
	$(".checker-group .add-row").first().before($(".inline-related.checker:not(.empty-form)"));
	// hide all order number inputs
	$('.checker-group .inline-related').find('input[id$=order]').parent('div').parent('div').hide();
	// turn cursor into crosshair over the handels
	$('.checker-group .inline-related h3').css('cursor', 'move');
}

function updateOrder() {
	// fill each order field with the current possition
	$(".checker-group").find(".checker").each(function(i) {
		$(this).find('input[id$=order]').val(i+1);
  });
}
