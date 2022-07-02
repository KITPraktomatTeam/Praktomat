# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

import django.utils.timezone

from io import BytesIO
import base64

import collections
import csv

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes

from tasks.models import Task
from taskstatistics.models import TasksStatistic

#@register.filter
#def index(list, i):
    #return List(int(i))

#@register.filter
#def entry_num_array(List):
    #return range(len(List))

def getQuerySet():
    # take only those Tasks into statistic which have been published.
    # ToDo: maybe we should shrink to Tasks which have been expired ...
    #       than change task__publication_date__lte to task__submission_date__lte
    # additional filter be "all_checker_finished"
    # so in Boxplot-Diagramm we can be sure, that a possible user can see valid data.
    # this filters must keep in sync with filters inside function prepare_statistic_data
    now = django.utils.timezone.now()
    return TasksStatistic.objects.filter(task__publication_date__lte = now , task__all_checker_finished = True).values(
    "id",
    "task_id",
    "title",
    "submitters_all",
    "submitters_passed_finals",
    "submitters_failed_finals",
    "submitters_latest_not_accepted",
    "uploads_all",
    "uploads_accepted",
    "uploads_rejected",
    # the following datas are information about how many submissions did users done until they finally passed
    "avg_upl_until_final_pass",
    "lo_whisker_upl_til_final_pass",
    "lo_quart_upl_til_final_pass",
    "med_upl_til_final_pass",
    "up_quart_upl_til_final_pass",
    "up_whisker_upl_until_final_pass",
    # the following data are information about how many uploads did users to pass pretests but failing in posttest.
    "avg_uploads_final_failed",
    "lo_whisker_upl_final_fail",
    "lo_quart_upl_final_fail",
    "median_uploads_final_failed",
    "up_quart_upl_final_failed",
    "up_whisker_upl_final_failed",
    # the following data are information about how many failed uploads did users done before they gave up.
    "avg_uploads_only_failed",
    "lo_whisker_upl_only_fail",
    "lo_quart_upl_only_fail",
    "median_uploads_only_failed",
    "up_quart_upl_only_failed",
    "up_whisker_upl_only_failed").order_by('id')

def boxblot_to_graphic_list(glist=None, dtupel=None, fliers=None):
    if ((glist is None) or (dtupel is None)):
        raise TypeError("boxblot_to_graphic_list cannot be called with None in the first two arguments")
    if not isinstance(fliers, dict):
        raise TypeError("Third argument fliers of boxblot_to_graphic_list must be dict or None")
    if fliers is not None and fliers:
        assert dtupel.task_id == max(fliers["task_id"]) , "dtupel.task_id: %s vs fliers[task_id]:%s"%(str(dtupel.task_id),str(max(fliers["task_id"])))

        assert fliers["status"][0] in ["prefailed", "postpassed", "postfailed"]
        #print(type(fliers), fliers)

    fig1, ax1 = plt.subplots()
    ax1.set_title("Task %d : %s\n Submitters passed Posttest: %d \n Submitters passed Pretest but failed Posttest: %d\n Submitters failed Pretest: %d\n Uploads accepted: %d\n Uploads rejected: %d"%(dtupel.task_id , str(dtupel.title) , dtupel.submitters_passed_finals if dtupel.submitters_passed_finals else 0, dtupel.submitters_failed_finals if dtupel.submitters_failed_finals else 0, dtupel.submitters_latest_not_accepted if dtupel.submitters_latest_not_accepted else 0, dtupel.uploads_accepted if dtupel.uploads_accepted else 0, dtupel.uploads_rejected if dtupel.uploads_rejected else 0 ))
    #list of dicts used for mydata:
    dummyuserupload = dict()
    if fliers is not None and fliers:
        dummyuserupload = { fliers["status"][0]: [max(fliers["uploads"])]}
        #print(dummyuserupload)
        #if "postpassed" in dummyuserupload:
            #print("bla1" , dummyuserupload["postpassed"])

        #if "postfailed" in dummyuserupload:
            #print("bla2", dummyuserupload["postfailed"])

        #if "prefailed" in dummyuserupload:
            #print("bla3", dummyuserupload["prefailed"])
    mydata = [
       {'med' : dtupel.med_upl_til_final_pass if dtupel.med_upl_til_final_pass is not None  else 0 ,
        'q1':   dtupel.lo_quart_upl_til_final_pass if dtupel.lo_quart_upl_til_final_pass is not None  else 0,
        'q3': dtupel.up_quart_upl_til_final_pass if dtupel.up_quart_upl_til_final_pass is not None else 0,
        'whislo': dtupel.lo_whisker_upl_til_final_pass if dtupel.lo_whisker_upl_til_final_pass is not None else 0,
        'whishi': dtupel.up_whisker_upl_until_final_pass if dtupel.up_whisker_upl_until_final_pass is not None else 0,
        'mean': dtupel.avg_upl_until_final_pass if dtupel.avg_upl_until_final_pass is not None else 0,
        'fliers': dummyuserupload["postpassed"] if "postpassed" in dummyuserupload and dummyuserupload["postpassed"][0]>0 else [],
        'label': "posttest\n passed"
       },
       {'med' : dtupel.median_uploads_final_failed if dtupel.median_uploads_final_failed is not None else 0,
        'q1': dtupel.lo_quart_upl_final_fail if dtupel.lo_quart_upl_final_fail is not None else 0,
        'q3': dtupel.up_quart_upl_final_failed if dtupel.up_quart_upl_final_failed is not None else 0,
        'whislo': dtupel.lo_whisker_upl_final_fail if dtupel.lo_whisker_upl_final_fail is not None else 0,
        'whishi': dtupel.up_whisker_upl_final_failed if dtupel.up_whisker_upl_final_failed is not None else 0,
        'mean': dtupel.avg_uploads_final_failed if dtupel.avg_uploads_final_failed  is not None else 0,
        'fliers': dummyuserupload["postfailed"] if "postfailed" in dummyuserupload  and dummyuserupload["postfailed"][0]>0  else [],
        'label': "posttest\n failed"
        },
       {'med' : dtupel.median_uploads_only_failed if dtupel.median_uploads_only_failed is not None else 0,
        'q1': dtupel.lo_quart_upl_only_fail if dtupel.lo_quart_upl_only_fail is not None else 0,
        'q3': dtupel.up_quart_upl_only_failed if dtupel.up_quart_upl_only_failed is not None else 0,
        'whislo': dtupel.lo_whisker_upl_only_fail if dtupel.lo_whisker_upl_only_fail is not None else 0,
        'whishi': dtupel.up_whisker_upl_only_failed if dtupel.up_whisker_upl_only_failed is not None else 0,
        'mean': dtupel.avg_uploads_only_failed if dtupel.avg_uploads_only_failed is not None else 0,
        'fliers': dummyuserupload["prefailed"] if "prefailed" in dummyuserupload and dummyuserupload["prefailed"][0]>0 else [],
        'label': "pretest\n failed"
       }
    ]
    #print(mydata)
    bpd = ax1.bxp(bxpstats=mydata, showmeans=True) # is a call to matplotlib.axes.Axes.bxp
    if fliers is None or not fliers or (dummyuserupload[fliers["status"][0]][0] == 0):
        #print("Legende Uploads:" , dummyuserupload[fliers["status"][0]][0])
        ax1.legend([bpd['medians'][0], bpd['means'][0]], ['median', 'mean'])
    else:
        #print("Legende Uploads:" , type(dummyuserupload[fliers["status"][0]][0]), dummyuserupload[fliers["status"][0]][0] )
        ax1.legend([bpd['medians'][0], bpd['means'][0] ,bpd['fliers'][0]], ['median', 'mean', 'your position'])
    plt.ylabel("Anzahl der Uploads pro Person")
    plt.xlabel("Kategorien der jeweils letzten Einreichungen von Studierenden")
    #additional message to figure
    msg=""
    plt.text(0.5 , 0.05 , msg , fontsize=20)
    plt.tight_layout()
    bytebuffer = BytesIO()
    plt.savefig(bytebuffer, format='png')
    bytebuffer.seek(0) # set stream position to begin of buffer.
    image_png=bytebuffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    bytebuffer.close()
    #plt.show()
    glist.append(graph)
    return glist

def prepare_statistic_data():
    now = django.utils.timezone.now()
    # define the order of colums
    queryset= getQuerySet().values()
    cols = TasksStatistic._meta.get_fields()
    objects_list = []
    for row in queryset:
        ordered_dict = collections.OrderedDict()
        for col in cols:
            if str(col.name) in ["task" , "task_id"]:
                ordered_dict["task_id"] = row["task_id"]
            else:
                ordered_dict[col.name] = row[col.name]
        objects_list.append(ordered_dict)
    tasks = Task.objects.filter(publication_date__lte = now, all_checker_finished = True).order_by('id')
    return (objects_list , tasks)

def prepare_graphic_list(data_,userdata_=None):
    #create boxplot-Diagramms using values from DataFrame
    #for each task create tree Boxplots in one diagramm
    # liste der spalten überschriften für zeilenzugriff und liste der Zeilennummern : df.iloc[spalte][Zeile]
    if data_ is None or len(data_)==0:
        return list()
    #print("data_: ", type(data_), dir(data_), data_)

    df = pd.DataFrame.from_dict(data_).set_index("id")
    graphic_list_ = []
    for row in df.itertuples(index=False,name="TaskStatisticData"):
        boxblot_to_graphic_list(glist=graphic_list_, dtupel=row, fliers=userdata_[row.task_id] if userdata_ is not None and row.task_id in userdata_ else dict())
    return graphic_list_


# Create your views here.
def tasks_statistic(request):
    data_ , tasks_ = prepare_statistic_data()
    ddupl = dict() # dict of dictionaries containing information for task uploads of current user, only filled if there is a current user
    if hasattr(request, "user") and request.user is not None and request.user.is_authenticated:
        current_user=request.user
        finaluploads = [(t, t.final_solution(request.user)) for t in tasks_]
        for (t, f) in finaluploads:
            d = { "task_id":[],"status":[],"uploads":[]}
            d["task_id"].append(t.pk)
            d["status"].append("prefailed" if f is None else ("postpassed" if f.accepted else "postfailed"))
            d["uploads"].append(0 if f is None else f.number)
            ddupl[t.pk] = d
    graphic_list_ = prepare_graphic_list(data_=data_, userdata_=ddupl)
    if len(data_) <= 0:
        messages.warning(request, "Apparently no data available...")
    return render(request,'taskstatistics/overview.html', {'data':data_ , 'graphics':graphic_list_})


def tasks_statistic_download(request):
    #data_ = getQuerySet()
    #df = pd.DataFrame.from_records(data_.values())
    data_ , tasks_ = prepare_statistic_data()
    if len(data_) <= 0:
        messages.warning(request, "Apparently no data available...")
        return render(request,'taskstatistics/overview.html', {'data':data_})
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="TaskStatistic.csv"'
    writer = csv.writer(response, delimiter=str(",") , quotechar=str('"'))
    df = pd.DataFrame.from_dict(data_)
    df.to_csv(path_or_buf=response,index=False)
    #Das Folgende geht mit SQlite Backend nicht!
    #from django.db import connection
    #objects_qs=getQuerySet().values()
    #cursor = connection.cursor()
    #print(type(cursor))
    #
    #cursor.copy_to(response, "(" + str(objects.query) + ")", null="", sep=",")
    #
    return response
