from django.conf import settings as S
from core.models import Notification

def settings(request):
    data = {
        "build": S.LATEST_BUILD,
        "debug": S.DEBUG
    }
    if request.user.is_authenticated:
        data['notifications'] = Notification.objects.filter(
            user=request.user
        ).order_by('-id')[:10]
    return data