from abandoned.models import AbandonedObject, AbandonedObjectCategory
from cities_light.contrib.restframework3 import City, Country, Region


def get_all_objects():
    return AbandonedObject.objects.all()


def get_all_categories():
    return AbandonedObjectCategory.objects.all()


def get_available_objects_for_user(user):
    if user.is_superuser:
        return get_all_objects()
    return AbandonedObject.objects.filter(hidden=False)


def get_all_cities():
    return City.objects.all()


def get_all_countries():
    return Country.objects.all()
