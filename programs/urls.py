from django.urls import path
from . import views


urlpatterns = [
    path('fuel_index', views.fuel_index, name='fuel_index'),
    path('note_index', views.note_index, name='note_index'),
    path('fuel_processing', views.fuel_processing, name='fuel_processing'),
]
