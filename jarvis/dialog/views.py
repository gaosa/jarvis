from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from . import model_helper as MH
from . import query_answer as QA
import json as JSON

def index(request):
    return HttpResponse("Hello, please specify the dialog id.")


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
