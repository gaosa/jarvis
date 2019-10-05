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

Run

```bash
python manage.py runserver
```

And point your browser to

```
http://localhost:8000/
```

Upload a valid csv file of your own. You will be redirected to an url like:

```
http://localhost:8000/1/
```

Try typing some commands after `>`,
and hit `Enter`! 

Your command will be parsed and some results will be returned.