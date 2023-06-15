from django.urls import path
from abandoned.views import *

urlpatterns = [
    path('objects/', AbandonedObjectListCreateAPIView.as_view()),
    path('objects/<int:pk>', AbandonedObjectRetrieveAPIView.as_view())
]
