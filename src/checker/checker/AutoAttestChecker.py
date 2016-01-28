# -*- coding: utf-8 -*-

"""
Dump files containing input, expected output and the shell script running diff.
"""

import os
import os.path

from django.db import models
from django.utils.translation import ugettext_lazy as _
from checker.models import Checker, CheckerResult, execute_arglist
from django.utils.html import escape
from utilities.file_operations import *
from accounts.models import User
from attestation.models import RatingScaleItem, Attestation
from datetime import datetime

class AutoAttestChecker(Checker):

    author = models.ForeignKey(User, verbose_name="attestation author", limit_choices_to = {'groups__name': 'Tutor'})
    public_comment = models.TextField(blank=True, help_text = _('Comment which is shown to the user.'))
    private_comment = models.TextField(blank=True, help_text = _('Comment which is only visible to tutors'))
    final = models.BooleanField(default = False, help_text = _('Indicates whether the attestation is ready to be published'))
    published = models.BooleanField(default = False, help_text = _('Indicates whether the user can see the attestation.'))

    def __init__(self, *args, **kwargs):
        super(AutoAttestChecker, self).__init__(*args, **kwargs)
        self._meta.get_field_by_name('always')[0].default = False
        self._meta.get_field_by_name('public')[0].default = False

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
        
        result = CheckerResult(checker=self)
        result.set_passed(checkers_failed == 0)
        grades = list(self.task.final_grade_rating_scale.ratingscaleitem_set.all())
        for a in Attestation.objects.filter(solution=env.solution(), author=self.author):
            a.delete()
        if checkers_failed == 0:
            if checkers_passed > 0:
                result.set_log('All %d required checkers passed.' % checkers_passed)
            else:
                result.set_log('WARNING: No checkers.')
            a = Attestation(solution=env.solution(), author=self.author,
                            public_comment=self.public_comment, private_comment=self.private_comment,
                            final=self.final, published=self.published, published_on=datetime.now(),
                            final_grade=grades[-1])
        else:
            result.set_log('%d required checkers failed.' % checkers_failed)
            a = Attestation(solution=env.solution(), author=self.author,
                            public_comment=self.public_comment, private_comment=self.private_comment,
                            final=self.final, published=self.published, published_on=datetime.now(),
                            final_grade=grades[0])
        a.save()
        
        return result
    
from checker.admin import    CheckerInline

class AutoAttestInline(CheckerInline):
    model = AutoAttestChecker
