"""Core module for answering commands
"""


from . import model_helper as MH
from . import grapher as G
from . import parser as P
from django.core.files.storage import default_storage
import pandas as pd


# Format: {dialog_id: (DataFrame, colNames, graph, paramDict)}
_cache = {}

# What parameters are required for generating a graph
requiredKeysDict = {
    'basic': ['x', 'y', 'type']
}


def _init(dialog_id):
    df = pd.read_pickle(default_storage.path(str(dialog_id)))
    colNames = list(df.columns)
    graph = None
    try:
        graph = G.load(MH.get_latest_graph_json_str(dialog_id))
    except:
        graph = None
    paramDict = MH.get_param_dict(dialog_id)
    return (df, colNames, graph, paramDict)


def _get(dialog_id):
    if dialog_id not in _cache:
        _cache[dialog_id] = _init(dialog_id)
    return _cache[dialog_id]


def _set(dialog_id, df, colNames, graph, paramDict):
    _cache[dialog_id] = (df, colNames, graph, paramDict)


def _check_params(paramKeys, paramType):
    '''Check whether all the parameters for a specific param type is set.
    For example, for paramType == 'basic', required keys are x, y, and type
    '''
    missingParams = []
    for key in requiredKeysDict[paramType]:
        if key not in paramKeys:
            missingParams.append(key)
    return missingParams


def _update_param_dict(paramDict, newParams, stage):
    '''Returns what parameter is missing if applicable
    '''
    if stage == 1:
        # First stage
        if 'completed' in paramDict:
            del paramDict['completed']
        if 'current' in paramDict:
            del paramDict['current']
        if 'basic' not in paramDict:
            paramDict['basic'] = {}
        for key in newParams:
            paramDict['basic'][key] = newParams[key]
        return _check_params(paramDict['basic'].keys(), 'basic')
    else:
        # Second stage
        if 'basic' not in paramDict:
            return _check_params([], 'basic')
        if len(paramDict['basic']) != len(requiredKeysDict['basic']):
            return _check_params(paramDict['basic'].keys(), 'basic')
        # Basic parameters are good
        return []


def _query_for_missing_params(missingParams):
    return "What should be the value for {}?".format(missingParams[0])


def handle_command(dialog_id, command):
    MH.append_command(dialog_id, command)
    df, colNames, graph, paramDict = _get(dialog_id)
    # Recognize...
    stage, newParams = P.parse(colNames, command)
    missingParams = _update_param_dict(paramDict, newParams, stage)
    if len(missingParams) != 0:
        MH.append_query(dialog_id, _query_for_missing_params(missingParams))
    else:
        # Draw
        if stage == 1:
            graph = G.draw_basic(df, paramDict['basic'])
        else:
            graph = G.draw_incremental(graph, paramDict)
        # Save to database
        MH.append_query(dialog_id, 'OK, I think this is the graph you want:')
        MH.append_graph(dialog_id, graph.to_json())
        MH.append_query(dialog_id, 'What else do you want to do?')
    MH.set_param_dict(dialog_id, paramDict)
    # Update cache
    _set(dialog_id, df, colNames, graph, paramDict)
