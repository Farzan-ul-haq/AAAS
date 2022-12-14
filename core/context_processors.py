from django.conf import settings as S


def settings(request):
    return {
        "build": S.LATEST_BUILD,
        "debug": S.DEBUG
    }