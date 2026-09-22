from django.conf import settings


def maptiler(request):
    return {
        "MAPTILER_API_KEY": settings.MAPTILER_API_KEY,
    }