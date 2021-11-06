from django.contrib import admin
from django.db import models
from .models import Settings, Chunk

from tinymce.widgets import TinyMCE

class ChunkInline(admin.StackedInline):
    model = Chunk
    fields = ('content',)
    max_num = 0        # don't allow adds
    can_delete = False

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

class SettingsAdmin(admin.ModelAdmin):

    fieldsets = (
            ('Registration', {
                'fields': (
                    ( 'email_validation_regex',
                      'mat_number_validation_regex'),
                    'deny_registration_from',
                    'acount_activation_days',
                    ( 'account_manual_validation',
                      'requires_disclaimer_acceptance',
                      'new_users_via_sso' )
                )
            }),
            ('Solutions and Attestations', {
                'fields': (
                    'accept_all_solutions',
                    'anonymous_attestation',
                    'attestation_allow_run_checkers',
                    ('final_grades_arithmetic_option',
                     'final_grades_plagiarism_option')
                )
            }),
            ('Attestation Publishing/Viewing', {
                 'fields': (
                     'invisible_attestor',
                     'attestation_reply_to',
                 )
            })
        )
    inlines = [ChunkInline]

    def has_add_permission(self, request):
        return False

admin.site.register(Settings, SettingsAdmin)
