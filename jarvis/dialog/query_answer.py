"""Core module for answering commands
"""


from . import model_helper as MH
from . import grapher as G


def handle_command(dialog_id, command):
    MH.append_command(dialog_id, command)
    MH.append_query(dialog_id, 'OK, I think this is the graph you want:')
    graphJson = G.getJsonString()
    MH.append_graph(dialog_id, graphJson)
    MH.append_query(dialog_id, 'What else do you want to do?')