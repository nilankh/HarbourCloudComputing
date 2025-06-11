from django.urls import path
from .views import BookShiftsView

urlpatterns = [
    path("book-shifts/", BookShiftsView.as_view(), name="book-shifts")
]