from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from . import model_helper as MH
from . import query_answer_new as QA
from . import test_prepare as TP
import json as JSON
import pandas as pd


@csrf_exempt
def index(request):
    if request.method == 'GET':
        return render(request, 'dialog/index.html', {
                "data": JSON.dumps({
                    "url": reverse('index'),
                })
        })
    else:
        df = None
        if 'fileName' in request.FILES:
            f = request.FILES['fileName']
            fname = default_storage.save(f.name, f)
            try:
                df = pd.read_csv(default_storage.path(fname))
            except Exception as e:
                return JsonResponse({
                    'msg': str(e)
                })
            dialog_id = MH.create_dialog()
            df.to_pickle(default_storage.path(str(dialog_id)))
            MH.append_query(dialog_id, 'Hi there! What can I do for you?')
            return JsonResponse({
                'url': str(dialog_id)
            })
        else:
            k, v = TP.prepare(request)
            return JsonResponse({k: v}) 


@csrf_exempt
def dialog(request, dialog_id):
    if request.method == 'GET':
        return render(request, 'dialog/dialog.html', {
            "data": JSON.dumps({
                "dialog_id": dialog_id,
                "records": MH.get_records_for_dialog(dialog_id),
                "current_url": reverse('dialog', args=[dialog_id]),
            })
        })
    elif request.method == 'POST':
        id_max = MH.get_max_record_id(dialog_id)
        command = JSON.loads(request.body.decode('utf-8'))['command']
        QA.handle_command(dialog_id, command)
        return JsonResponse({
            'new_records': MH.get_records_for_dialog(dialog_id, id_max)
        })
    else:
        return "NULL"


def json(request, json_id):
    return JsonResponse(MH.get_json(json_id))
