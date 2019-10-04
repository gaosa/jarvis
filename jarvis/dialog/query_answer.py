"""Core module for answering commands
"""


from . import model_helper as MH
from . import grapher as G
from . import parser as P
from django.core.files.storage import default_storage
import pandas as pd


# Format: {dialog_id: (DataFrame, colNames, graph, paramDict)}
_cache = {}


def _init(dialog_id):
    df = pd.to_pickle(default_storage.path(str(dialog_id)))
    colNames = list(df.columns)
    graph = None
    try:
        graph = G.load(MH.get_latest_graph_json_str(dialog_id))
    except:
        graph = None
    paramDict = MH.get_param_dict(dialog_id)
    return (df, colNames, graph)


def _get(dialog_id):
    if dialog_id not in _cache:
        _cache[dialog_id] = _init(dialog_id)
    return _cache[dialog_id]


def _set(dialog_id, df, colNames, graph, paramDict):
    _cache[dialog_id] = (df, colNames, graph, paramDict)


def _update_param_dict(paramDict, newParams):
    pass


def handle_command(dialog_id, command):
    MH.append_command(dialog_id, command)
    df, colNames, graph, paramDict = _get(dialog_id)
    # Recognize...
    newParams = P.parse(colNames, command)
    _update_param_dict(paramDict, newParams)
    # Draw.. (if applicable)
    graph, msg = G.draw(df, )
    # Save to database
    MH.append_query(dialog_id, 'OK, I think this is the graph you want:')
    MH.append_graph(dialog_id, graph.to_json())
    MH.append_query(dialog_id, 'What else do you want to do?')
    MH.set_param_dict(dialog_id, paramDict)
    # Update cache
    _set(dialog_id, df, colNames, graph, paramDict)
