from django.contrib import admin
from attestation.models import *
from django.urls import reverse
from django.utils.html import format_html

import attestation.views

admin.autodiscover()

class RatingScaleItemInline(admin.TabularInline):
    model = RatingScaleItem
    extra = 0


class RatingScaleAdmin(admin.ModelAdmin):
    model = RatingScale
    inlines = [RatingScaleItemInline]

    class Media:
        js = (
              'frameworks/jquery/jquery.js',
              'frameworks/jquery/jquery-ui.js',
              'frameworks/jquery/jquery.tinysort.js',
              'script/rating_scale_sort.js',
        )

admin.site.register(RatingScale, RatingScaleAdmin)

admin.site.register(RatingAspect)


class AnnotatedSolutionFileAdminInline(admin.StackedInline):
    model = AnnotatedSolutionFile
    fields = ('content',)
    extra, max_num  = 0, 0
    can_delete = False

class RatingResultAdminInline(admin.StackedInline):
    model = RatingResult
    fields = ('mark',)
    extra, max_num  = 0, 0
    can_delete = False

class AttestationAdmin(admin.ModelAdmin):
    model = Attestation
    readonly_fields = ('created', 'show_solution',)
    fields = ( 'show_solution', 'author', 'created', 'public_comment', 'private_comment', 'final_grade', 'final', 'published', 'published_on')
    list_display = ('solution', 'author', 'created', 'final', 'published', 'published_on')
    list_filter = ('final', 'published', 'author', 'solution__author', 'solution__task')
    inlines = (RatingResultAdminInline, AnnotatedSolutionFileAdminInline)
    actions = ['export_attestations']

    def export_attestations(self, request, queryset):
        """ Export Attestation action """
        from django.http import HttpResponse
        response = HttpResponse(Attestation.export_Attestation(queryset), content_type="application/xml")
        response['Content-Disposition'] = 'attachment; filename=AttestationExport.xml'
        return response

    def get_form(self, request, obj=None, **kwargs):
        request.obj = obj
        return super(AttestationAdmin, self).get_form(request, obj,**kwargs)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "final_grade":
            kwargs["queryset"] = RatingScaleItem.objects.filter(scale__id=request.obj.solution.task.final_grade_rating_scale.id)
        return super(AttestationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def show_solution(self, instance):
        return format_html('<a href="{0}">{1}</a> by <a href="{2}">{3}</a>',
                           reverse('admin:solutions_solution_change', args=(instance.solution.pk,)),
                           instance.solution,
                           reverse('admin:accounts_user_change', args=(instance.solution.author.pk,)),
                           instance.solution.author,
                          )
    show_solution.short_description = 'Solution'


    def get_urls(self):
        """ Add URL to Attestation update """
        urls = super(AttestationAdmin, self).get_urls()
        from django.conf.urls import url
        my_urls = [url(r'^update/$', attestation.views.update_attestations, name='attestation_update')]
        return my_urls + urls

    def has_add_permission(self, request):
        return False

admin.site.register(Attestation, AttestationAdmin)


class RatingAdminInline(admin.StackedInline):
    """ used in task as inline """
    model = Rating
    extra = 0
