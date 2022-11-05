from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        if request.user.mode == 'S':
            return redirect('seller:dashboard')
        if request.user.mode == 'B':
            return redirect('buyer:dashboard')
    else:
        return render(request, 'core/index.html')
