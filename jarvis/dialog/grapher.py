import altair as alt
from . import model_helper as MH
from django.core.files.storage import default_storage


def draw_basic(df, paramDict):
    x = paramDict['x']
    y = paramDict['y']
    graph_type = paramDict['type']
    chart = eval('alt.Chart(df).mark_{}()'.format(graph_type))
    chart = chart.encode(x=x, y=y).interactive()
    return chart


def draw_incremental(chart, paramDict):
    pass


def load(json_str):
    return alt.Chart.from_json(json_str)

