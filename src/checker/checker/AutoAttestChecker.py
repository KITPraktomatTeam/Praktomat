# -*- coding: utf-8 -*-

"""
AutoAttestChecker (based on code of S.B. (HBRS FB02,2013) updated by Robert Hartmann,HBRS FB02, 2013 - 2016,2020,2022)
"""
import os, re
import os.path

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
#from django.utils.encoding import force_unicode
from checker.basemodels import Checker, CheckerFileField, CheckerResult, truncated_log
from django.core.exceptions import ValidationError
from utilities.safeexec import execute_arglist
from utilities.file_operations import *

from accounts.models import User
from attestation.models import RatingScaleItem, Attestation
from datetime import datetime

class AutoAttestChecker(Checker):

    author = models.ForeignKey(User, verbose_name="attestation author", limit_choices_to = {'groups__name': 'Tutor'}, on_delete=models.SET_NULL, null=True, blank=True)
    public_comment = models.TextField(blank=True, help_text = _('Comment which is shown to the user.'))
    private_comment = models.TextField(blank=True, help_text = _('Comment which is only visible to tutors'))
    final = models.BooleanField(default = True, help_text = _('Indicates whether the attestation is ready to be published'))
    published = models.BooleanField(default = True, help_text = _('Indicates whether the user can see the attestation.'))

    def __init__(self, *args, **kwargs):
        super(AutoAttestChecker, self).__init__(*args, **kwargs)
        self._meta.get_field('always').default = False
        self._meta.get_field('public').default = False
        self._meta.get_field('required').default = False
        self._meta.get_field('final').default = True
        self._meta.get_field('published').default = True

    def clean(self):
        super(AutoAttestChecker, self).clean()
        if (self.required or self.always or self.public): raise ValidationError("Robert says: AutoAttestChecker have to be non-required, non-always, non-public")

    def title(self):
        """ Returns the title for this checker category. """
        return u"Attestation eintragen, wenn alle bisherigen Checker erfolgreiches Ergebnis hatten."

    @staticmethod
    def description():
        """ Returns a description for this Checker. """
        return u"Dies ist keine Prüfung, sondern trägt eine automatische Attestation ein."

    def run(self, env):
        """ Runs tests in a special environment. Here's the actual work.
        Returning CheckerResult. """

        checkers_passed = 0
        checkers_failed = 0
        for r in env.solution().checkerresult_set.all():
            if r.required():
                if r.passed:
                    checkers_passed += 1
                else:
                    checkers_failed += 1

	#result = CheckerResult(checker=self)
        result = CheckerResult(checker=self,solution=env.solution())
        result.set_passed(checkers_failed == 0)


        if User.objects.filter(id=self.author_id).count() == 0:
            self.author_id = None    # warum nicht self.author ???
            return result

	# delete all old own Attestations for this solution.
        for a in Attestation.objects.filter(solution=env.solution(), author=self.author):
            a.delete()

        # reset final/published attestations
        for a in Attestation.objects.filter(solution__task=env.solution().task, solution__author=env.solution().author):
            a.final = False
            a.published = False
            a.save()

        # reset final solution
        s = env.solution().task.final_solution(env.solution().author)
        if s:
            s.final = False
            s.save()

        # create new attestation
        if self.task.final_grade_rating_scale:
            grades = list(self.task.final_grade_rating_scale.ratingscaleitem_set.all())
            if checkers_failed == 0:
                if checkers_passed > 0:
                    result.set_log('All %d required checkers passed.' % checkers_passed)
                else:
                    result.set_log('WARNING: No checkers.')

                new_final_solution = env.solution()
                if new_final_solution:
                    new_final_solution.final = True
                    new_final_solution.save()

                a = Attestation(solution=env.solution(), author=self.author,
                                public_comment=self.public_comment, private_comment=self.private_comment,
                                final=self.final, published=self.published, published_on=datetime.now(),
                                final_grade=grades[-1])
                a.save()
            else:
                result.set_log('%d required checkers failed.' % checkers_failed)
#                result.set_solution_id(env.solution())
                a = Attestation(solution=env.solution(), author=self.author,
                                public_comment=self.public_comment, private_comment=self.private_comment,
                                final=self.final, published=self.published, published_on=datetime.now(),
                                final_grade=grades[0])
                a.save()
        return result

from checker.admin import    CheckerInline

class AutoAttestInline(CheckerInline):
    model = AutoAttestChecker
