from django.shortcuts import render, HttpResponse , redirect
#from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from .forms import createuserform
from django.contrib import messages
from django.contrib.auth import authenticate, logout as dj_logout, login as dj_login

from core.models import User

# Create your views here.

def test(request):
    return HttpResponse('HELLo test')


def base(request):
    if request.user.is_authenticated:
        return HttpResponse(request.user.username)
    else:
        return redirect('login')


def register(request):
    form = createuserform()
    if request.method=="POST":
        form = createuserform(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,'Account Created...')
            dj_login(request, user)
            mode = 'buyer' if user.mode == 'B' else "seller"
            return redirect(f"{mode}:dashboard")

    return render(request,'accounts/register.html', {
        'form': form
    })


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user= authenticate(request, username=username, password=password)

        if user is not None:
            dj_login(request, user)
            mode = 'buyer' if user.mode == 'B' else "seller"
            return redirect(f"{mode}:dashboard")
        else:
            messages.info(request,'Username Or Password is incorrect')
    context={}
    return render(request,'accounts/login.html',context)


def logout(request):
    dj_logout(request)
    return redirect('core:index')


def user_profile(request):
    if request.user.is_authenticated:
        context={}
        return render(request, 'accounts/user_profile.html', context)
    else:
        return HttpResponse('please login with your credentials to view user profile page ')