from django.contrib import admin
from django.urls import path, include
from abandoned.views import *

urlpatterns = [
    path('objects/', AbandonedObjectListCreateAPIView.as_view()),
    path('objects/<int:pk>', AbandonedObjectRetrieveAPIView.as_view())
]
