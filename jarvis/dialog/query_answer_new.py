from . import model_helper as MH
from django.core.files.storage import default_storage
import pandas as pd
from .jarvis.jarvis import Jarvis
import json


'''
Format:
<dialog_id: (Jarvis object, drawing commands)>
'''
__cache = {}


def __init_jarvis(dialog_id):
    df = pd.read_pickle(default_storage.path(str(dialog_id)))
    j = Jarvis(df)
    p = MH.get_predicate(dialog_id)
    if p != '':
        j.handle_next(p)
    return j


def __get(dialog_id):
    if dialog_id in __cache:
        return __cache[dialog_id]
    j = __init_jarvis(dialog_id)
    cmds = []
    for c in MH.get_commands(dialog_id):
        if __is_draw_command(c):
            j.handle_next(c)
            cmds.append(c)
        else:
            c = c.lower()
            if c == 'undo':
                j = __init_jarvis(dialog_id)
                cmds = cmds[:-1]
                for cc in cmds:
                    j.handle_next(cc)
            elif c == 'reset':
                j = __init_jarvis(dialog_id)
                cmds = []
    __cache[dialog_id] = j, cmds
    return j, cmds


def __is_draw_command(command):
    return command.lower() not in ['undo', 'reset', 'sample']


def __is_graph_equal_to_target(dialog_id, json_str):
    target = MH.get_target_graph_json(dialog_id)
    dic1 = json.loads(json_str)
    dic2 = json.loads(target)
    for k in dic1:
        if dic1[k] != dic2[k]:
            print(k, dic1[k], dic2[k])
    return target != '' and json.loads(json_str) == json.loads(target)

def handle_command(dialog_id, command):
    j, cmds = __get(dialog_id)
    MH.append_command(dialog_id, command)
    if __is_draw_command(command):
        cmds.append(command)
        success, err_msgs = j.handle_next(command)
        for msg in err_msgs:
            MH.append_query(dialog_id, msg)
        if success:
            MH.append_query(dialog_id, 'Here is the graph I generated...')
            MH.append_graph(dialog_id, j.get().to_json())
            if __is_graph_equal_to_target(dialog_id, j.get().to_json()):
                MH.append_query(dialog_id, 'Congratulations! You have generated the target graph.')
            MH.append_query(dialog_id, 'What else would you like to do?')
    else:
        command = command.lower()
        if command == 'undo':
            j = __init_jarvis(dialog_id)
            cmds = cmds[:-1]
            print(cmds)
            for c in cmds:
                j.handle_next(c)
            __cache[dialog_id] = j, cmds
            MH.append_query(dialog_id, 'Undo done!')
            MH.append_graph(dialog_id, j.get().to_json())
        elif command == 'reset':
            j = __init_jarvis(dialog_id)
            __cache[dialog_id] = j, []
            MH.append_query(dialog_id, 'Reset done!')
            MH.append_graph(dialog_id, j.get().to_json())
        elif command == 'sample':
            MH.append_query(dialog_id, 'Here are samples of the data...')
            MH.append_query(dialog_id, str(pd.read_pickle(default_storage.path(str(dialog_id))).sample(n=5, random_state=1)))
        if __is_graph_equal_to_target(dialog_id, j.get().to_json()):
            MH.append_query(dialog_id, 'Congratulations! You have generated the target graph.')
        MH.append_query(dialog_id, 'What else would you like to do?')
