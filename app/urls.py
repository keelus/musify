from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('', view=views.index_page, name="index_page"),
]
