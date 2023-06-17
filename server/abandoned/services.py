from abandoned.models import AbandonedObject, AbandonedObjectCategory


def get_all_objects():
    return AbandonedObject.objects.all()


def get_all_categories():
    return AbandonedObjectCategory.objects.all()


def get_available_objects_for_user(user):
    if user.is_superuser:
        return get_all_objects()
    return AbandonedObject.objects.filter(hidden=False)
