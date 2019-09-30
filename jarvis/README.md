# How to start

First, please install [Django](https://docs.djangoproject.com/en/2.2/topics/install/).

```bash
# 1. Clone this repository
git clone https://github.com/gaosa/jarvis.git

# 2. Enter into Django project folder
cd jarvis/jarvis

# 3. Set up database
python manage.py migrate
```

# To play with some mock data

Enter the Django shell

```bash
python manage.py shell
```

Copy and paste the following command to the shell

```python
from dialog.models import *
dialog = Dialog.objects.create()
Record.objects.create(dialog=dialog, record_type='Q', content='Hello! What can I do for you?')
Record.objects.create(dialog=dialog, record_type='A', content='Can you give me some sample graph?')
Record.objects.create(dialog=dialog, record_type='Q', content='Sure! Here is one graph:')
Record.objects.create(dialog=dialog, record_type='G', content='{"config": {"view": {"width": 400, "height": 300}, "mark": {"tooltip": null}}, "data": {"url": "https://vega.github.io/vega-datasets/data/cars.json"}, "mark": "point", "encoding": {"color": {"type": "nominal", "field": "Origin"}, "x": {"type": "quantitative", "field": "Horsepower"}, "y": {"type": "quantitative", "field": "Miles_per_Gallon"}}, "selection": {"selector002": {"type": "interval", "bind": "scales", "encodings": ["x", "y"]}}, "$schema": "https://vega.github.io/schema/vega-lite/v3.4.0.json"}')
Record.objects.create(dialog=dialog, record_type='Q', content='What else can I do for you?')
```

Then run

```bash
python manage.py runserver
```

And point your browser to

```
http://localhost:8000/1/
```

You will see some results!

You can then type in some commands after `>` and hit `Enter`. Currently your command will be stored, and some fake results will be provided.