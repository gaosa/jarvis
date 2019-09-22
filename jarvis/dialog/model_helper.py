"""This module communicates to models

Saves data into model, or get data from model
"""

from django.db.models import Max
from django.urls import reverse
from .models import Dialog, Record
import json as JSON


def get_records_for_dialog(dialog_id, greater_than_id=-1):
    records = []
    for r in Dialog.objects.get(id=dialog_id).record_set.filter(id__gt=greater_than_id).order_by('id'):
        if r.record_type != 'G':
            records.append([r.record_type, r.content])
        else:
            records.append([r.record_type, reverse('json', args=[r.id])])
    return records


def append_command(dialog_id, command):
    Record.objects.create(dialog=Dialog.objects.get(id=dialog_id), record_type='A', content=command)


def get_json(json_id):
    return JSON.loads(Record.objects.get(id=json_id).content)


def get_max_record_id(dialog_id):
    return Dialog.objects.get(id=dialog_id).record_set.aggregate(Max('id'))['id__max']