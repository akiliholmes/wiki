from django.urls import path

from . import views

app_name="encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>/wiki/", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("<str:title>/edit/", views.edit, name="edit"),
    path("new/", views.new, name="new")
    ]
