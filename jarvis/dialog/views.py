from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Dialog, Record
import json

def index(request):
    return HttpResponse("Hello, please specify the dialog id.")

def dialog(request, record_id):
    return render(request, 'dialog/dialog.html')

def json(request, json_id):
    return JsonResponse(json.loads(Record.objects.get(id=json_id).content))
