from django.urls import path
from . import views
urlpatterns = [
    path(
        '',
        views.symptom_checker,
        name='symptom_checker'
    ),
]