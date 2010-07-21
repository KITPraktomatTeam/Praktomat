from django.db import models
from praktomat.tasks.models import Task
from praktomat.solutions.models import Solution, SolutionFile
from django.utils.translation import ugettext_lazy as _
import difflib

from praktomat.accounts.models import User

class Attestation(models.Model):
	""""""

	created = models.DateTimeField(auto_now_add=True, editable=False)
	solution = models.ForeignKey(Solution, editable=False)
	author = models.ForeignKey(User, editable=False)

	public_comment = models.TextField(blank=True, help_text = _('Comment which is shown to the user.'))
	private_comment = models.TextField(blank=True, help_text = _('Comment which is only visible to tutors'))
	final_grade = models.CharField(blank=True, max_length=100,  help_text = _('The final grade only visible to tutors.'))
	
	final = models.BooleanField(default = False, help_text = _('Indicates whether the attestation is ready to be published'))
	published = models.BooleanField(default = False, help_text = _('Indicates whether the user can see the attestation.'))

class AnnotatedSolutionFile(models.Model):
	""""""
	attestation = models.ForeignKey(Attestation)
	solution_file = models.ForeignKey(SolutionFile)
	content = models.TextField(help_text = _('The content of the solution file annotated by the tutor.'))
	
	def has_anotations(self):
		original = self.solution_file.content()
		anotated = self.content.replace("\r","")
		return not original == anotated
	
	def content_diff(self):
		d = difflib.Differ()
		original = self.solution_file.content().splitlines(1)
		anotated = self.content.replace("\r","").splitlines(1)
		result = list(d.compare(original, anotated))
		return "".join(result)
	
	def __unicode__(self):
		return self.solution_file.__unicode__()
	
class RatingAspect(models.Model):
	""" describes an review aspect which the reviewer has to evaluate """	
	name = models.CharField(max_length=100, help_text = _('The Name of the Aspect to be rated. E.g.: "Readabylity"'))
	description = models.TextField(help_text = _('Description of the Aspect and how it should be rated. E.w.: "How well is the code structured?"'))
	
	def __unicode__(self):
		return self.name

class RatingScale(models.Model):
	""" describes a scale upone which the reviewer rates the aspect """
	name = models.CharField(max_length=100, help_text = _('The Name of the rating scale for the aspects. E.g.: "School marks"'))
	
	def __unicode__(self):
		return self.name
	
class RatingScaleItem(models.Model):
	""" lists all items(marks) of an rating scale"""	
	scale = models.ForeignKey(RatingScale)
	name = models.CharField(max_length=100, help_text = _('The Name of the item(mark) in the rating scale. E.g.: "A" or "very good" '))
	position = models.PositiveSmallIntegerField(help_text = _('Defines the order in which the items are sorted. Lowest is best.'))
	
	def __unicode__(self):
		return self.name

class Rating(models.Model):
	""" intermediate model to assign a rating aspect and a rating scale to a task """
	task = models.ForeignKey(Task)
	aspect = models.ForeignKey(RatingAspect)
	scale = models.ForeignKey(RatingScale)
		
class RatingResult(models.Model):
	""" the rating of particular aspect of a specific solution """
	attestation = models.ForeignKey(Attestation)
	aspect = models.ForeignKey(RatingAspect)
	mark = models.ForeignKey(RatingScaleItem, null=True) # allow for db-null so that rating results can be created programaticly without mark (blank = False !)
	
class Script(models.Model):
	""" save java script function of the rating overview page """
	script = models.TextField(	help_text = _("This JavaScript will calculate a recommend end note for every user based on final grade of every task."), default="""var sum = 0;\nfor (x in grades) {\n\tsum += parseInt(grades[x]);\n}\nresult=Math.round(sum/grades.length);""")
	
	