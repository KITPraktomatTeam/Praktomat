/* menu-sort.js */

jQuery(function($) {
   $('div.inline-group').sortable({
	  /*containment: 'parent', zindex: 10, */
	  items: 'div.inline-related',
	  handle: 'h3:first',
	  update: function() {
		$(this).find('div.inline-related').each(function(i) {
			  $(this).find('input[id$=position]').val(i+1);
		});
	   }
   });
   $('div.inline-related h3').css('cursor', 'move');
   $('div.inline-related').find('input[id$=position]').parent('div').parent('div').hide();
   });