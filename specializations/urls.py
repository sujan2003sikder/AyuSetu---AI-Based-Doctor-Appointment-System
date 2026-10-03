from django.urls import path

from . import views


urlpatterns = [

    path('',views.specialization_list,name='specialization_list'),
    path('<int:specialization_id>/doctors/',views.specialization_doctors, name='specialization_doctors'),

]