from . import model_helper as MH
from django.core.files.storage import default_storage
from vega_datasets import data
import altair as alt
import pandas as pd
import numpy as np

src1 = pd.DataFrame({
    'project': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
    'score': [28, 55, 43, 91, 81, 53, 19, 87, 52]
})

src2_x, src2_y = np.meshgrid(range(-5, 5), range(-5, 5))
src2_z = src2_x ** 2 + src2_y ** 2

# Convert this grid to columnar data expected by Altair
src2 = pd.DataFrame({'a': src2_x.ravel(),
                     'b': src2_y.ravel(),
                     'c': src2_z.ravel()})


tests = {
    'test1-1': [
        data.cars(),
        ('Q', 'Welcome to Jarvis!'),
        ('G', alt.Chart(data.cars()).mark_circle(opacity=0.9).encode(x='Horsepower',y='Miles_per_Gallon').to_json()),
        ('Q', 'Can you draw the above graph with natural language?'),
    ],
    'test1-2': [
        data.cars(),
        ('Q', 'Welcome to Jarvis!'),
        ('G', alt.Chart(data.cars()).mark_circle(opacity=0.9).encode(x='Horsepower',y='Miles_per_Gallon').to_json()),
        ('G', alt.Chart(data.cars()).mark_circle(opacity=0.5).encode(x='Horsepower',y='Miles_per_Gallon').to_json()),
        ('Q', 'Can you convert from the upper graph to the lower graph?'),
        ('P', 'scatterplot miles per gallon by horsepower')
    ],
    'test1-3': [
        data.cars(),
        ('Q', 'Welcome to Jarvis!'),
        ('G', alt.Chart(data.cars()).mark_circle(opacity=0.9).encode(x='Horsepower',y='Miles_per_Gallon').to_json()),
        ('G', alt.Chart(data.cars()).mark_circle(opacity=0.9).encode(x='Horsepower',y='Miles_per_Gallon',color='Origin').to_json()),
        ('Q', 'Can you convert from the upper graph to the lower graph?'),
        ('P', 'scatterplot miles per gallon by horsepower')
    ],
    'test2-1': [
        src1,
        ('Q', 'Welcome to Jarvis!'),
        ('G', alt.Chart(src1).mark_bar(opacity=0.9).encode(x='project',y='score').to_json()),
        ('Q', 'Can you draw the above graph with natural language?'),
    ],
    'test2-2': [
        src1,
        ('Q', 'Welcome to Jarvis!'),
        ('G', alt.Chart(src1).mark_bar(opacity=0.9).encode(x='project',y='score').to_json()),
        ('G', alt.Chart(src1).mark_bar(opacity=0.9).encode(x='project',y='score',tooltip=['score']).to_json()),
        ('Q', 'Can you convert from the upper graph to the lower graph? (Please move over the second graph)'),
        ('P', 'bar chart score by project')
    ],
    'test2-3': [
        src1,
        ('Q', 'Welcome to Jarvis!'),
        ('G', alt.Chart(src1).mark_bar(opacity=0.9).encode(x='project',y='score').to_json()),
        ('G', alt.Chart(src1).mark_bar(opacity=0.9,color='red').encode(x='project',y='score').to_json()),
        ('Q', 'Can you convert from the upper graph to the lower graph?'),
        ('P', 'bar chart score by project')
    ],
    'test3-1': [
        src2,
        ('Q', 'Welcome to Jarvis!'),
        ('G', alt.Chart(src2).mark_rect().encode(
            x='a:O',
            y='b:O',
            color='c:Q'
        ).to_json()),
        ('Q', 'Can you draw the above graph with natural language?'),
    ],
    'test3-2': [
        src2,
        ('Q', 'Welcome to Jarvis!'),
        ('G', alt.Chart(src2).mark_rect().encode(
            x='a:O',
            y='b:O',
            color='c:Q'
        ).to_json()),
        ('G', alt.Chart(src2).mark_circle().encode(
            x='a:O',
            y='b:O',
            size='c:Q',
            color='c:Q'
        ).to_json()),
        ('Q', 'Can you convert from the upper graph to the lower graph?'),
        ('P', 'rectangle x is a y is b color is c')
    ],
    'test3-3': [
        src2,
        ('Q', 'Welcome to Jarvis!'),
        ('G', alt.Chart(src2).mark_rect().encode(
            x='a:O',
            y='b:O',
            color='c:Q'
        ).to_json()),
        ('G', alt.Chart(src2).mark_rect().encode(
            x='a:O',
            y='b:O',
            color='c:Q'
        ).properties(width=400*1.2, height=300*1.2).to_json()),
        ('Q', 'Can you convert from the upper graph to the lower graph?'),
        ('P', 'rectangle x is a y is b color is c')
    ],
}


def prepare(request):
    keys = list(request.POST.keys())
    if len(keys) != 1:
        return 'msg', 'Invalid request'
    
    testName = keys[0]
    if testName in tests:
        dialog_id = MH.create_dialog()
        tests[testName][0].to_pickle(default_storage.path(str(dialog_id)))
        for r in tests[testName][1:]:
            if r[0] == 'Q':
                MH.append_query(dialog_id, r[1])
            elif r[0] == 'G':
                MH.append_graph(dialog_id, r[1])
            elif r[0] == 'P':
                MH.set_predicate(dialog_id, r[1])
        return 'url', str(dialog_id)
    
    return 'msg', 'Invalid request'

