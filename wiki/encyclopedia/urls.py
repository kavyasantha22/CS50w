from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create_page", views.create_page, name="create_page"),
    path("edit_page/<str:name>", views.edit_page, name="edit_page"),
    path("entry/<str:name>", views.entry, name="entry"),
    path("random_page", views.random_page, name="random_page")
]
