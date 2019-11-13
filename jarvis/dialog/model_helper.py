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


def get_commands(dialog_id):
    return [r.content for r in Record.objects.filter(dialog__id=dialog_id, record_type='A')]


def append_query(dialog_id, query):
    Record.objects.create(dialog=Dialog.objects.get(id=dialog_id), record_type='Q', content=query)


def append_graph(dialog_id, graph):
    Record.objects.create(dialog=Dialog.objects.get(id=dialog_id), record_type='G', content=graph)


def get_json(json_id):
    return JSON.loads(Record.objects.get(id=json_id).content)


def get_max_record_id(dialog_id):
    return Dialog.objects.get(id=dialog_id).record_set.aggregate(Max('id'))['id__max']


def create_dialog():
    return Dialog.objects.create().id


def get_latest_graph_json_str(dialog_id):
    return Record.objects.filter(dialog__id=2, record_type='G').order_by('-id')[0].content


def get_param_dict(dialog_id):
    return JSON.loads(Dialog.objects.get(id=dialog_id).paramDictString)


def set_param_dict(dialog_id, paramDict):
    dialog = Dialog.objects.get(id=dialog_id)
    dialog.paramDictString = JSON.dumps(paramDict)
    dialog.save()


def get_predicate(dialog_id):
    return Dialog.objects.get(id=dialog_id).predicate


def set_predicate(dialog_id, predicate):
    d = Dialog.objects.get(id=dialog_id)
    d.predicate = predicate
    d.save()

def set_target_graph_json(dialog_id, json_str):
    d = Dialog.objects.get(id=dialog_id)
    d.target = json_str
    d.save()

def get_target_graph_json(dialog_id):
    return Dialog.objects.get(id=dialog_id).target
