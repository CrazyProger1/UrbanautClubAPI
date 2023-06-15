from django.contrib import admin
from django.urls import path, include
from abandoned.views import *

urlpatterns = [
    path('objects/', AbandonedObjectListAPIView.as_view())
]
