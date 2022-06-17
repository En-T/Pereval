from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('add/', submitData),
    path('pereval/<int:pk>', get_submitData_id),
    path('edit/<int:pk>', patch_submitData_id),
    path('pereval/<str:email>', get_submitData_email),

]
