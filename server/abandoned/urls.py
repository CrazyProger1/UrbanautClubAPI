from django.urls import path, include
from abandoned.views import *

urlpatterns = [
    path('', include('cities_light.contrib.restframework3')),
    path('objects/', AbandonedObjectListCreateAPIView.as_view()),
    path('objects/<int:pk>', AbandonedObjectRetrieveAPIView.as_view()),
    path('objects/categories/', AbandonedObjectCategoryListAPIView.as_view())
]
