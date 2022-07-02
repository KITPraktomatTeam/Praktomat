# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# We create a model for an unmanaged database view: The database view gets constructed by RAW-SQL commands inside Praktomat/src/statistics/migrations/0001_initial.py
class TasksStatistic(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey('tasks.Task',on_delete=models.DO_NOTHING)
    title = models.CharField(help_text='The name of the Task', max_length=100)
    submitters_all = models.BigIntegerField() # is the number of users, who had done at least one upload for that task
    submitters_passed_finals = models.BigIntegerField() # is the number of users, who passed sucessfully all pre and post tests after submission date has been over for that task
    submitters_failed_finals = models.BigIntegerField() # is the number of users, who failed in the post tests after submission date has been over for that task
    submitters_latest_not_accepted = models.BigIntegerField()  # is the number of users, who failed in the pre tests at uploadtime and don't have any final solution after submission date has been over for that task
    uploads_all = models.BigIntegerField() # is the number of all failed or passed submissions
    uploads_accepted = models.BigIntegerField() # is the number of all passed submissions
    uploads_rejected = models.BigIntegerField() # is the number of all failed submissions
    # the following datas are information about how many submissions did users done until they finally passed
    avg_upl_until_final_pass = models.BigIntegerField(verbose_name='avg uploads until final passed')
    lo_whisker_upl_til_final_pass = models.BigIntegerField(verbose_name='lower whisker uploads until final passed')
    lo_quart_upl_til_final_pass = models.BigIntegerField(verbose_name='lower quartiel uploads until final passed')
    med_upl_til_final_pass = models.BigIntegerField(verbose_name='median uploads until final passed')
    up_quart_upl_til_final_pass = models.BigIntegerField(verbose_name='upper quartiel uploads until final passed')
    up_whisker_upl_until_final_pass = models.BigIntegerField(verbose_name='upper whisker uploads until final passed')
    # the following data are information about how many uploads did users to pass pretests but failing in posttest.
    avg_uploads_final_failed= models.BigIntegerField()
    lo_whisker_upl_final_fail = models.BigIntegerField(verbose_name='lower whisker uploads final failed')
    lo_quart_upl_final_fail = models.BigIntegerField(verbose_name='lower quartiel uploads final failed')
    median_uploads_final_failed = models.BigIntegerField()
    up_quart_upl_final_failed = models.BigIntegerField(verbose_name='upper quartiel uploads final failed')
    up_whisker_upl_final_failed = models.BigIntegerField(verbose_name='upper whisker uploads final failed')
    # the following data are information about how many failed uploads did users done before they gave up.
    avg_uploads_only_failed= models.BigIntegerField()
    lo_whisker_upl_only_fail = models.BigIntegerField(verbose_name='lower whisker uploads only failed')
    lo_quart_upl_only_fail = models.BigIntegerField(verbose_name='lower quartiel uploads only failed')
    median_uploads_only_failed = models.BigIntegerField()
    up_quart_upl_only_failed = models.BigIntegerField(verbose_name='upper quartiel uploads only failed')
    up_whisker_upl_only_failed = models.BigIntegerField(verbose_name='upper whisker uploads only failed')
    class Meta:
         managed = False
         db_table = 'dbview_tasksstatistic'
