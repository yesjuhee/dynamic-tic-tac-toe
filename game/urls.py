from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user/<int:cell_index>/", views.user, name="user"),
    path("computer/", views.computer, name="computer"),
]
