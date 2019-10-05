import re


supported_graph_type = {
    'scatterplot': 'circle',
    'scatter plot': 'circle',
    'point chart': 'circle',
    'circle chart': 'circle'
}


def _get_graph_type(command):
    for t in supported_graph_type:
        if t in command:
            return supported_graph_type[t]
    return None


def _get_x_y(colNames, command):
    g = re.match(r'.*\Wby (\w+)', command)
    y = None
    if g and g.group(1) in colNames:
        y = g.group(1)
    x = None
    for c in command.strip().split(' '):
        c.strip()
        if c in colNames:
            x = c
    return x, y


def parse(colNames, command):
    '''Returns (stage, paramDict)
    There are two stages: one and two.
    Stage 1: Only x, y, and style are required
    Stage 2: Incremental changes
    '''
    graph_type = _get_graph_type(command)
    x, y = _get_x_y(colNames, command)
    res = {}
    if graph_type:
        res['type'] = graph_type
    if x:
        res['x'] = x
    if y:
        res['y'] = y
    if len(res):
        # Stage 1
        return 1, res
    # Stage 2
    return 2, res
