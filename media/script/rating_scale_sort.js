

$(document).ready(function(){

	// hide all order number inputs
	$('td.position').hide();
	$("th:contains('Position')").hide();

	// remove double name
	$("td.original p").hide();			  
	$(".has_original").removeClass("has_original");
				  
	// change cursor
	$(".dynamic-ratingscaleitem_set").css('cursor', 'move');

	// apply sortebility
	$("tbody").sortable({
        items: '.dynamic-ratingscaleitem_set',
		revert: true,
		update: function() { 
			$(".dynamic-ratingscaleitem_set").each(function(i) {
				$(this).toggleClass("row1", i%2==0 );
				$(this).toggleClass("row2", i%2==1 );
			})
		}
    });
	
  	// On save: fill positions into textbox
	$("input[type=submit]").click(function() { 
			$(".dynamic-ratingscaleitem_set").each(function(i) {
				$(this).find('input[id$=position]').val(i);
			})
	})
});


