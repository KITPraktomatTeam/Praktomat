from django.db import models, transaction
from django.conf import settings
from tasks.models import Task
from solutions.models import Solution, SolutionFile
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage
from django.core import serializers
from django.template import loader
from django.contrib.sites.requests import RequestSite
from django.contrib import messages
from datetime import datetime
from utilities.nub import nub
import difflib
import tempfile
import zipfile

from accounts.models import User
from configuration import get_settings



class Attestation(models.Model):
	""""""

	created = models.DateTimeField(auto_now_add=True)
	solution = models.ForeignKey(Solution)
	author = models.ForeignKey(User, verbose_name="attestation author", limit_choices_to = {'groups__name': 'Tutor'})

	public_comment = models.TextField(blank=True, help_text = _('Comment which is shown to the user.'))
	private_comment = models.TextField(blank=True, help_text = _('Comment which is only visible to tutors'))
	final_grade = models.ForeignKey('RatingScaleItem', null=True, help_text = _('The mark for the whole solution.'))
	
	final = models.BooleanField(default = False, help_text = _('Indicates whether the attestation is ready to be published'))
	published = models.BooleanField(default = False, help_text = _('Indicates whether the user can see the attestation.'))
	published_on = models.DateTimeField(blank=True,null=True,help_text = _('The Date/Time the attestation was published.'))
	
	def publish(self, request, by):
		""" Set attestation to published and send email to user """
		self.published = True
		self.published_on = datetime.now()
		self.save()

                email = self.solution.author.email
                if not email:
                    return

		# Send confirmation email
                t = loader.get_template('attestation/attestation_email.html')
                c = {
                        'attest': self,
                        'protocol': request.is_secure() and "https" or "http",
                        'domain': RequestSite(request).domain,
                        'site_name': settings.SITE_NAME,
                        'by': by,
                        'invisible_attestor' : get_settings().invisible_attestor,
                        }
                subject = _("New attestation for your solution of the task '%s'") % self.solution.task
                body = t.render(c)
                reply_to = ([self.author.email]                    if self.author.email and (not get_settings().invisible_attestor) else []) \
                         + ([get_settings().attestation_reply_to]  if get_settings().attestation_reply_to else [])
                headers = {'Reply-To': ', '.join(reply_to)} if reply_to else None
                email = EmailMessage(subject, body, None, (email,), headers = headers)
                email.send()

        def withdraw(self, request, by):
		self.published = False
                self.final = False
		self.published_on = datetime.now()
		self.save()

                recps = nub([
                    self.solution.author, # student
                    self.author,          # attestation writer
                    by,                   # usually attestation writer, may be trainer
                    ] + list(User.objects.filter(groups__name="Trainer"))  # and, for withdrawals, all trainers
                    )
                emails = [u.email for u in recps if u.email]

                if not emails:
                    return

		# Send confirmation email
                t = loader.get_template('attestation/attestation_withdraw_email.html')
                c = {
                        'attest': self,
                        'protocol': request.is_secure() and "https" or "http",
                        'domain': RequestSite(request).domain,
                        'site_name': settings.SITE_NAME,
                        'by': by,
                        }
                subject = _("Attestation for your solution of the task '%s' withdrawn") % self.solution.task
                body = t.render(c)
                recipients = emails[0:1]
                bcc_recipients = emails[1:]
                email = EmailMessage(subject, body, None, recipients, bcc_recipients)
                email.send()

	@classmethod
	def export_Attestation(cls, qureyset):
		""" Serializes an Attestation queryset to xml """
		from solutions.models import Solution

		# fetch tasks, media objects, checker and serialize
		attestation_objects = list(qureyset)
		solution_objects = list([attestation.solution for attestation in attestation_objects])
		annotatedsolutionfiles_objects = list(AnnotatedSolutionFile.objects.filter(attestation__in = attestation_objects).defer('content'))
		for annotatedsolutionfile in annotatedsolutionfiles_objects:
			annotatedsolutionfile.content = ""
			annotatedsolutionfile._meta.model_name = "annotatedsolutionfile" # *sigh*
		solutionfile_objects = list([annotatedsolutionfile.solution_file for annotatedsolutionfile in annotatedsolutionfiles_objects])

		task_objects = list(set([attestation.solution.task for attestation in attestation_objects]))
		
		ratingresult_objects  = list(RatingResult.objects.filter(attestation__in = attestation_objects))
		aspect_grades_objects = set([ratingresult.mark for ratingresult in ratingresult_objects])
		final_grades_objects  = set([attestation.final_grade for attestation in attestation_objects])
		rating_objects        = set([ratingresult.rating for ratingresult in ratingresult_objects])
 		aspect_objects        = set([rating.aspect for rating in rating_objects])
		ratingscale_objects = list(
			  set(RatingScale.objects.filter(ratingscaleitem__in = final_grades_objects | aspect_grades_objects))
		)
		ratingscaleitems_objects = list(RatingScaleItem.objects.filter(scale__in = ratingscale_objects))

		data = serializers.serialize("xml", attestation_objects + solution_objects + ratingscale_objects + ratingscaleitems_objects + ratingresult_objects + list(rating_objects) + list(aspect_objects) + annotatedsolutionfiles_objects + solutionfile_objects)
		
		return data

	@classmethod
	@transaction.atomic
	def update_Attestations(cls, request, xml_file):
		from solutions.models import Solution, SolutionFile
		data = xml_file.read()
		deserialized = list(serializers.deserialize("xml", data))

		tosave_attestation = []
		tosave_ratingresult = []
		

		for deserialized_object in deserialized:
			new_object = deserialized_object.object

			if isinstance(new_object, Attestation):
				old_object = Attestation.objects.get(id = new_object.id)
				
				if not(attributes_equal(new_object, old_object, ["solution"])):
					messages.error(request, "1Invalid change from " + str(old_object) + " to " + str(new_object) + ". Nothing was imported.")
					return
				tosave_attestation.append(deserialized_object)

			elif isinstance(new_object, RatingResult):
				old_object = RatingResult.objects.get(id = new_object.id)
				if not(attributes_equal(new_object, old_object, ["attestation", "rating"])):
					messages.error(request, "2Invalid change from " + str(old_object) + " to " + str(new_object) + ". Nothing was imported.")
					return
				tosave_ratingresult.append(deserialized_object)

			elif isinstance(new_object, AnnotatedSolutionFile):
				old_object = AnnotatedSolutionFile.objects.get(id = new_object.id)
				if not(attributes_equal(new_object, old_object, ["attestation", "solutionfile"])):
					messages.error(request, "4Invalid change from " + str(old_object) + " to " + str(new_object) + ". Nothing was imported.")
					return

			elif ( isinstance(new_object, Solution)
                            or isinstance(new_object, Rating)
                            or isinstance(new_object, RatingAspect)
                            or isinstance(new_object, RatingScale)
                            or isinstance(new_object, SolutionFile)
                            or isinstance(new_object, RatingScaleItem)):
				old_object = new_object.__class__.objects.get(id = new_object.id)
				if not(model_fields_equal(new_object, old_object)):
					messages.error(request, "3Invalid change from " + str(old_object) + " to " + str(new_object) + ". Nothing was imported.")
					return
			else:
				messages.error(request, "Invalid model class for: " + str(new_object) + ". Nothing was imported.")
				return

		for object in (tosave_attestation + tosave_ratingresult):
			object.save()
		
		messages.success(request, "Updated %d attestations, and %d rating results." % (len(tosave_attestation), len(tosave_ratingresult)))

		return
			


class AnnotatedSolutionFile(models.Model):
	""""""
	attestation = models.ForeignKey(Attestation)
	solution_file = models.ForeignKey(SolutionFile)
	content = models.TextField(help_text = _('The content of the solution file annotated by the tutor.'), blank = True)
	
	def has_anotations(self):
		original = self.solution_file.content().replace("\r\n","\n").replace("\r","\n")
		anotated = self.content.replace("\r\n","\n").replace("\r","\n")
		return not original == anotated
	
	def content_diff(self):
		d = difflib.Differ()
		original = self.solution_file.content().replace("\r\n","\n").replace("\r","\n").splitlines(0)
		anotated = self.content.replace("\r\n","\n").replace("\r","\n").splitlines(0)
		result = list(d.compare(original, anotated))
		return "\n".join(map(lambda l: l.strip("\n"), result))
	
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
	
	class Meta:
		ordering = ['position']
	
	def __unicode__(self):
		return self.name

class Rating(models.Model):
	""" intermediate model to assign a rating aspect and a rating scale to a task """
	task = models.ForeignKey(Task)
	aspect = models.ForeignKey(RatingAspect)
	scale = models.ForeignKey(RatingScale)
	
	def __unicode__(self):
		return "%s - %s - %s" % (self.task.title, self.aspect.name, self.scale.name)
		
class RatingResult(models.Model):
	""" the rating of particular aspect of a specific solution """
	attestation = models.ForeignKey(Attestation)
	rating = models.ForeignKey(Rating)
	mark = models.ForeignKey(RatingScaleItem, null=True) # allow for db-null so that rating results can be created programaticly without mark (blank = False !)

	def __unicode__(self):
		return unicode(self.rating.aspect) 
	
class Script(models.Model):
	""" save java script function of the rating overview page """
	script = models.TextField(blank=True, help_text = _("This JavaScript will calculate a recommend end note for every user based on final grade of every task."), default="""var sum = 0.0;\nfor (x = 0; x != grades.length; ++x) {\n    grade = parseFloat(grades[x]);\n    if (!isNaN(grade)) {\n        sum += grade;\n    }\n}\nresult=sum;""")
	



def attributes_equal(this,that,attrs):
	_NOTFOUND = object()
        for attr in attrs:
            v1, v2 = [getattr(obj, attr, _NOTFOUND) for obj in [this, that]]
            if (v1 is _NOTFOUND) != (v2 is _NOTFOUND):
		return False
            elif v1 != v2:
                return False
        return True

def model_fields_equal(this,that):
	this_fields = [field.name for field in this._meta.fields]
	that_fields = [field.name for field in that._meta.fields]
	return this_fields == that_fields and attributes_equal(this, that, this_fields)
