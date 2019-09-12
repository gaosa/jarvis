from django.urls import path
from . import views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:dialog_id>/', views.dialog, name='dialog'),
    path('json/<int:json_id>/', views.json, name='json')
]