from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Dialog, Record
import json as JSON

def index(request):
    return HttpResponse("Hello, please specify the dialog id.")

def dialog(request, dialog_id):
    records = []
    for r in Dialog.objects.get(id=dialog_id).record_set.all().order_by('id'):
        if r.record_type != 'G':
            records.append([r.record_type, r.content])
        else:
            records.append([r.record_type, reverse('json', args=[r.id])])
    return render(request, 'dialog/dialog.html', {
        "records": JSON.dumps(records)
    })

def json(request, json_id):
    return JsonResponse(JSON.loads(Record.objects.get(id=json_id).content))
