/* dynamic_inlines_with_sort.js */
/* Created in May 2009 by Hannes Rydén */
/* Use, distribute and modify freely */
/* http://www.djangosnippets.org/snippets/1489/ */


// "Add"-link html code. Defaults to Django's "+" image icon, but could use text instead.
add_link_html = '<img src="/media/img/admin/icon_addlink.gif" ' +
'width="10" height="10" alt="Add new row" style="margin:0.5em 1em;" />';
// "Delete"-link html code. Defaults to Django's "x" image icon, but could use text instead.
delete_link_html = '<img src="/media/img/admin/icon_deletelink.gif" ' +
'width="10" height="10" alt="Delete row" style="margin-top:0.5em" />';
position_field = 'position'; // Name of inline model field (integer) used for ordering. Defaults to "position".

jQuery(function($) {    
	   // This script is applied to all TABULAR inlines
	   $('div.inline-group').each(function() {
								  
								  // Hide initial extra row and prepare it to be used as a template for new rows
								  add_template = $(this).find('div.inline-related:last');
								  add_template.addClass('add_template').hide();
								  $(this).prepend(add_template);
								  
								  // Get rid of numbers: to difficult to replace later on
								  h3 = add_template.find('h3');
								  h3.html(h3.html().replace(/#[0-9]+/, ""));
								  b = add_template.find('h3>b');
								  b.html(b.html().replace(/:/, ""));
								  
								  // Hide model field 'changed'. hack to allow saving of new items without altering the default values od the model 
								  $(this).find('.form-row.changed').hide();
								  
								  // Hide initial deleted rows
								  $(this).find('span.delete input:checkbox:checked').parent('div').addClass('deleted_row').hide();
								  
								  // "Add"-button in bottom of inline for adding new rows
								  $(this).find('h2').append('<span class="add" style="position: absolute; right: 026px;"><a class="addlink add" href="#"></a></span>');
								  
								  $(this).find('a.add').click(function(){
															  old_item = $(this).parents('div.inline-group').find('div.add_template')
															  new_item = old_item.clone(true);
															  new_item.removeClass('add_template').show();
															  // update hidden value, so django will recognice new entrz even if the the default values were not changed
															  new_item.find('[id$=changed]:input').val('yes')
															  
															  $(this).parents('div.inline-group').append(new_item);
															  
															  update_positions($(this).parents('div.inline-group'), true);
															  
															  // Place for special code to re-enable javascript widgets after clone (e.g. an ajax-autocomplete field)
															  // Fictive example: new_item.find('.autocomplete').each(function() { $(this).triggerHandler('autocomplete'); });
															  }).removeAttr('href').css('cursor', 'pointer');
								  
								  // "Delete"-buttons for each row that replaces the default checkbox 
								  $(this).find('h3').each(function() {
														  create_delete_button($(this));
														  });
								  });
	   });

// Function for creating fancy delete buttons
function create_delete_button(header)
{
    // if the item has not been saved once create a span for the delete button 
	if (header.find('span.delete').length == 0) {
		header.append('<span class="delete"></span>')
	}	
	
	span = header.find('span.delete')
	
	// Replace checkbox with image
	span.find('label').hide();
	span.find('input:checkbox').hide();
	span.append('<a class="deletelink delete" href="#"></a>');
    
    span.find('a.delete').click(function(){
								current_element = $(this).parents('div.inline-related')
								current_group = current_element.parents('div.inline-group')
								deletebox = $(this).prevAll('input')
								if (deletebox.length != 0) // This row has already been saved once, so we must keep checkbox
								{
								deletebox.attr('checked', true);
								current_element.addClass('deleted_row').hide();
								}
								else // This row has never been saved so we can just remove the element completely
								{
								current_element.remove();
								}
								
								update_positions(current_group, true);
								}).removeAttr('href').css('cursor', 'pointer');
}

// Updates "position"-field values based on row order in table
function update_positions(group, update_ids)
{
	//    even = true
	num_rows = 0
	//    position = 0;
	
	//    // Set correct position: Filter through all trs, excluding first th tr and last hidden template tr
	//    group.find('div.inline-relatet:not(.add_template):not(.deleted_row)').each(function() {
	//        if (position_field != '')
	//        {
	//            // Update position field
	//            $(this).find('td.' + position_field + ' input').val(position + 1);
	//            position++;
	//        }
	//        else
	//        {
	//            // Update row coloring
	//            $(this).removeClass('row1 row2');
	//            if (even)
	//            {
	//                $(this).addClass('row1');
	//                even = false;
	//            }
	//            else
	//            {
	//                $(this).addClass('row2');
	//                even = true;
	//            }
	//        }
	//    });
    
	//    table.find('tbody tr.has_original').each(function() {
	//        num_rows++;
	//    });
	//    
	//    table.find('tbody tr:not(.has_original):not(.add_template)').each(function() {
	//        if (update_ids) update_id_fields($(this), num_rows);
	//        num_rows++;
	//    });    
	//    
	//    table.find('tbody tr.add_template').each(function() {
	//        if (update_ids) update_id_fields($(this), num_rows)
	//        num_rows++;
	//    });
	
	group.find('div.inline-related:not(.add_template)').each(function() {
															 if (update_ids) update_id_fields($(this), num_rows);
															 num_rows++;
															 }); 
	
	group.find('div.inline-related.add_template').each(function() {
													   if (update_ids) update_id_fields($(this), num_rows)
													   num_rows++;
													   });
	
	group.find("input[id$='TOTAL_FORMS']").val(num_rows);
}

// Updates actual id and name attributes of inputs, selects and so on.
// Required for Django validation to keep row order.
function update_id_fields(element, new_position)
{
    // Fix IDs, names etc.
    
    // <select ...>
    element.find('select').each(function() {
								// id=...
								old_id = $(this).attr('id').toString();
								new_id = old_id.replace(/([^ ]+\-)[0-9]+(\-[^ ]+)/i, "$1" + new_position + "$2");
								$(this).attr('id', new_id)
								
								// name=...
								old_id = $(this).attr('name').toString();
								new_id = old_id.replace(/([^ ]+\-)[0-9]+(\-[^ ]+)/i, "$1" + new_position + "$2");
								$(this).attr('name', new_id)
								});
    
    // <input ...>
    element.find('input').each(function() {
							   // id=...
							   old_id = $(this).attr('id').toString();
							   new_id = old_id.replace(/([^ ]+\-)[0-9]+(\-[^ ]+)/i, "$1" + new_position + "$2");
							   $(this).attr('id', new_id)
							   
							   // name=...
							   old_id = $(this).attr('name').toString();
							   new_id = old_id.replace(/([^ ]+\-)[0-9]+(\-[^ ]+)/i, "$1" + new_position + "$2");
							   $(this).attr('name', new_id)
							   });
    
    // <a ...>
    element.find('a').each(function() {
						   // id=...
						   old_id = $(this).attr('id').toString();
						   new_id = old_id.replace(/([^ ]+\-)[0-9]+(\-[^ ]+)/i, "$1" + new_position + "$2");
						   $(this).attr('id', new_id)
						   });
    
	// Are there other element types...? Add here.
				
    
}



