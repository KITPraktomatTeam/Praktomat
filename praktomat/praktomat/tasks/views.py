from praktomat.tasks.models import Task
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404 
from django.views.generic.list_detail import object_list, object_detail
from django.template.context import RequestContext
from datetime import datetime


@login_required
def taskList(Request):
	now = datetime.now()
	upcoming_tasks = Task.objects.filter(submission_date__gt = now).order_by('-submission_date')
	expired_tasks = Task.objects.filter(submission_date__lte = now).order_by('submission_date')
	return render_to_response('tasks/task_list.html',{'upcoming_tasks':upcoming_tasks, 'expired_tasks':expired_tasks}, context_instance=RequestContext(Request))
	#return object_list(Request, Task.objects.all(), template_object_name='tasks')

@login_required
def taskDetail(Request,task_id):
    return object_detail(Request, Task.objects.all(), task_id, template_object_name='task')

def taskPreview(Request):
    return render_to_response( 'tasks/task_preview.html',
                              {'description':Request.POST['data'],},
                              context_instance=RequestContext(Request))


	