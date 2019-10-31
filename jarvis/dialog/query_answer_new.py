from . import model_helper as MH
from django.core.files.storage import default_storage
import pandas as pd
from .jarvis.jarvis import Jarvis


'''
Format:
<dialog_id: Jarvis object>
'''
__cache = {}


def __get(dialog_id):
    if dialog_id in __cache:
        return __cache[dialog_id]
    df = pd.read_pickle(default_storage.path(str(dialog_id)))
    j = Jarvis(df)
    p = MH.get_predicate(dialog_id)
    if p != '':
        j.handle_next(p)
    for c in MH.get_commands(dialog_id):
        j.handle_next(c)
    __cache[dialog_id] = j
    return j


def handle_command(dialog_id, command):
    j = __get(dialog_id)
    MH.append_command(dialog_id, command)
    success, err_msgs = j.handle_next(command)
    for msg in err_msgs:
        MH.append_query(dialog_id, msg)
    if success:
        MH.append_query(dialog_id, 'Here is the graph I generated...')
        MH.append_graph(dialog_id, j.get().to_json())
        MH.append_query(dialog_id, 'What else would you like to do?')
