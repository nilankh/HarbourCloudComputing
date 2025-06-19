from django.urls import path
from .views import BookShiftsView
from . import views

urlpatterns = [
    path("book-shifts/", BookShiftsView.as_view(), name="book-shifts"),
    path("create_file/", views.create_file, name="create_file"),
    path("read_file/", views.read_file, name="read_file"),
    path("delete_file/", views.delete_file, name="delete_file"),
    path("get_file_size/", views.get_file_size, name="get_file_size"),
]
