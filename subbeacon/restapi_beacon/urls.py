from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from . import views


app_name = 'restapi_beacon'
urlpatterns = [
    path('', include('rest_framework.urls', namespace = 'rest_framework_category')),
    


]
