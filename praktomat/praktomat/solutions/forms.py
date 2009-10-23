from django.forms.models import ModelForm, inlineformset_factory

from praktomat.solutions.models import Solution, SolutionFile

class SolutionFileForm(ModelForm):
	class Meta:
		model = SolutionFile
		
	#def clean_file(self):
	#	data = self.cleaned_data['file']
	#	if (data.content_type = 'text/plain'):
	#		... .cpp file has 'application/octet-stream' !?  It would propably make sense to check the file ending 
	#		pass
	#	return data

SolutionFormSet = inlineformset_factory(Solution, SolutionFile, form=SolutionFileForm, can_delete=False, extra=8)