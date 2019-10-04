import altair as alt
from . import model_helper as MH
from vega_datasets import data


def draw(df, commandDict, chart = None):
    chart = alt.Chart(data.cars.url).mark_point().encode(
        x='Horsepower:Q',
        y='Miles_per_Gallon:Q',
        color='Origin:N'
    ).interactive()
    return (chart, '')


def load(json_str):
    return alt.Chart.from_json(json_str)

