"""Core module for answering commands
"""


from . import model_helper as MH


def handle_command(dialog_id, command):
    MH.append_command(dialog_id, command)