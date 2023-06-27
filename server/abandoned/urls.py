from django.urls import path, include
from abandoned.views import *

urlpatterns = [
    path('', include('cities_light.contrib.restframework3')),
    path('objects/', AbandonedObjectListCreateAPIView.as_view(), name='abandoned-objects'),
    path('objects/<int:pk>', AbandonedObjectRetrieveAPIView.as_view(), name='abandoned-object-detail'),
    path('objects/categories/', AbandonedObjectCategoryListAPIView.as_view(), name='abandoned-object-categories')
]
