var somethingWasChanged = false;
window.onbeforeunload = function() {
	if(somethingWasChanged)	return "You made changes on this page that you have not yet confirmed. If you navigate away from this page you will lose your unsaved changes.";
}

$(window).load(function () {
	$('#id_attest-public_comment').change(function(){somethingWasChanged=true;});
	$('#id_attest-private_comment').change(function(){somethingWasChanged=true;});
	$('#id_attest-final_grade').change(function(){somethingWasChanged=true;});
	$('#id_save').click(function(){somethingWasChanged=false;});
});

