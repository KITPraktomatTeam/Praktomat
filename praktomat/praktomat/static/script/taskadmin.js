$().ready(function() {
	  SyntaxHighlighter.config.clipboardSwf = '/static/script/syntaxhighlighter/scripts/clipboard.swf';
	  SyntaxHighlighter.all();
	  $('#id_description').tinymce({
			// Location of TinyMCE script
			script_url : '/static/script/tiny_mce/tiny_mce.js',
			
			// General options
			theme : "advanced",
			plugins : "safari,pagebreak,table,advhr,advimage,advlink,emotions,iespell,inlinepopups,media,searchreplace,print,contextmenu,paste,fullscreen,noneditable,visualchars,nonbreaking,syntaxhl",
			
			// Theme options
			theme_advanced_buttons1 : "formatselect,|,bold,italic,underline,strikethrough,|,forecolor,|,bullist,numlist,|,sub,sup,|,outdent,indent,blockquote,syntaxhl,|,visualchars,nonbreaking,|,link,unlink,anchor,image,cleanup,help,code,|,print,|,fullscreen",
			theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,undo,redo,|,tablecontrols,|,hr,removeformat,visualaid,|,charmap,emotions,iespell,media,advhr",
			theme_advanced_buttons3 : "",
			theme_advanced_buttons4 : "",					   
			theme_advanced_toolbar_location : "top",
			theme_advanced_toolbar_align : "left",
			theme_advanced_statusbar_location : "bottom",
			theme_advanced_resizing : true,
			extended_valid_elements : "textarea[cols|rows|disabled|name|readonly|class]" ,
			
			// Example content CSS (should be your site CSS)
			content_css : "/static/styles/style.css",
			
			// Drop lists for link/image/media/template dialogs
			template_external_list_url : "lists/template_list.js",
			external_link_list_url : "lists/link_list.js",
			external_image_list_url : "lists/image_list.js",
			media_external_list_url : "lists/media_list.js",
			
			// Replace values for the template plugin
			template_replace_values : {
			username : "Some User",
			staffid : "991234"
			}
			});
	  });
