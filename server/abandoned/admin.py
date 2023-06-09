from django.contrib import admin
from abandoned.models import *

admin.site.register(AbandonedObjectCategory)
admin.site.register(Coordinates)
admin.site.register(Address)
admin.site.register(AbandonedObject)
admin.site.register(AbandonedObjectLocation)