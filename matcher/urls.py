from django.urls import path
from . import views

app_name = 'matcher'

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze, name='analyze'),
    path('history/', views.history, name='history'),
]
