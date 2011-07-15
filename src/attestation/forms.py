# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.forms.models import ModelForm, inlineformset_factory, BaseInlineFormSet
from django.forms.formsets import formset_factory
from django import forms

from attestation.models import Attestation, AnnotatedSolutionFile, RatingResult, Script
from configuration.models import Settings
											

class AttestationForm(ModelForm):
	class Meta:
		model = Attestation
		exclude = ('solution', 'author', 'final', 'published')
		
	def __init__(self, *args, **kwargs): 
		super(AttestationForm, self).__init__(*args, **kwargs) 
		final_grade_rating_scale = kwargs['instance'].solution.task.final_grade_rating_scale
		if final_grade_rating_scale:
			self.fields['final_grade'].choices = [ (item['id'], item['name']) for item in final_grade_rating_scale.ratingscaleitem_set.values() ]
		else:
			del self.fields['final_grade']
	
class AttestationPreviewForm(ModelForm):
	class Meta:
		model = Attestation
		fields = ('final',)

class AnnotatedFileForm(ModelForm):
	class Meta:
		model = AnnotatedSolutionFile
		fields=('content',)
		
AnnotatedFileFormSet = inlineformset_factory(Attestation, AnnotatedSolutionFile, form=AnnotatedFileForm, formset=BaseInlineFormSet, can_delete=False, extra=0)


class RatingResultForm(ModelForm):
	def __init__(self, *args, **kwargs): 
		super(RatingResultForm, self).__init__(*args, **kwargs)
		ratingResult = kwargs['instance']
		self.fields['mark'].label = ratingResult.aspect.name 
		self.fields['mark'].help_text = ratingResult.aspect.description 
		# beware, the following line is kind of creepy
		self.fields['mark'].choices = [ (item['id'], item['name']) for item in ratingResult.attestation.solution.task.rating_set.get(aspect=ratingResult.aspect).scale.ratingscaleitem_set.values() ]
	
	class Meta:
		model = RatingResult
		fields=('mark',)

RatingResultFormSet = inlineformset_factory(Attestation, RatingResult, form=RatingResultForm, formset=BaseInlineFormSet, can_delete=False, extra=0)

class ScriptForm(ModelForm):
	class Meta:
		model = Script

class PublishFinalGradeForm(ModelForm):
	class Meta:
		model = Settings
		fields = ('final_grades_published',)