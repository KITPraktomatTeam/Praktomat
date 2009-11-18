from django.db import models
from django.contrib.auth.models import User
from praktomat.tasks.models import Task
from praktomat.solutions.models import Solution, SolutionFile
from django.utils.translation import ugettext_lazy as _

class Attestation(models.Model):
	""""""

	created = models.DateTimeField(auto_now_add=True)
	solution = models.ForeignKey(Solution)
	author = models.ForeignKey(User)

	public_comment = models.TextField(help_text = _('Comment which is shown to the user.'))
	private_comment = models.TextField(help_text = _('Comment which is only visible to tutors'))
	final_grade = models.CharField(max_length=2,  help_text = _('The final grade only visible to tutors.'))
	
	final = models.BooleanField(default = False, help_text = _('Indicates whether the tutor has finished the review process.'))
	
	
	

class AnnotatedSolutionFile(models.Model):
	""""""

	attestation = models.ForeignKey(Attestation)
	solution_file = models.ForeignKey(SolutionFile)
	content = models.TextField(help_text = _('The content of the solution file annotated by the tutor.'))