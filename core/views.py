from django.shortcuts import render, redirect
from django.conf import settings

def index(request): # landing page
    """Landing Page"""
    ## COMMENTING FOR NOW
    # if request.user.is_authenticated:
    #     if request.user.mode == 'S':
    #         return redirect('seller:dashboard')
    #     if request.user.mode == 'B':
    #         return redirect('buyer:dashboard')
    # else:
    #     return render(request, 'core/index.html')
    return render(request, 'core/index.html')

def explore(request): # this contains the list of products
    """This contains the list of products"""
    return render(request, 'core/explore.html')



def project_plan(request): # ONLY FOR DEVs
    return render(request, 'core/plan.html')
