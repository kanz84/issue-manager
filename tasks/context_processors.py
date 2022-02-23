from django.conf import settings as django_settings


def settings(_):
    return {
        "settings": django_settings,
    }
