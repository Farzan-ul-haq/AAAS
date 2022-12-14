from django.shortcuts import render, redirect
from django.conf import settings

def index(request):
    if request.user.is_authenticated:
        if request.user.mode == 'S':
            return redirect('seller:dashboard')
        if request.user.mode == 'B':
            return redirect('buyer:dashboard')
    else:
        debug = settings.DEBUG
        return render(request, 'core/index.html', {
            'debug': debug
        })


def project_plan(request): # ONLY FOR DEVs
    build = settings.LATEST_BUILD
    return render(request, 'core/plan.html', {
        "build": build
    })
