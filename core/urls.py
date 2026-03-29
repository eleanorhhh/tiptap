# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('load_all/', views.get_all_notes, name='load_all_notes'),
    path('save/', views.save_note, name='save_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
]