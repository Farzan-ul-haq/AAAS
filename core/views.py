from django.shortcuts import render, redirect
from django.conf import settings

def index(request):
    if request.user.is_authenticated:
        if request.user.mode == 'S':
            return redirect('seller:dashboard')
        if request.user.mode == 'B':
            return redirect('buyer:dashboard')
    else:
        return render(request, 'core/index.html')


def project_plan(request): # ONLY FOR DEVs
    return render(request, 'core/plan.html')
