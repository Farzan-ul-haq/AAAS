from django.shortcuts import render, HttpResponse , redirect
#from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from .forms import createuserform
from django.contrib import messages
from django.contrib.auth import authenticate, logout as dj_logout, login as dj_login

from core.models import User

# Create your views here.

def test(request):
    """
    """
    return HttpResponse('HELLo test')


def base(request):
    if request.user.is_authenticated:
        return HttpResponse(request.user.username)
    else:
        return redirect('login')


def register(request):
    """
    REGISTER:
        GET CREATE USER FORM
        IF POST:
            CHECK FORM VALIDITY
            IF VALID CREATE USER
            LOGIN THE CREATED USER
            REDIRECT TO DASHBOARD
    """
    form = createuserform()
    if request.method=="POST":
        form = createuserform(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,'Account Created...')
            dj_login(request, user)

            redirect_to = request.session.get('redirect_to', None) # IF REDIRECT URL: MARKETED CUSTOMER
            if redirect_to:
                del request.session['redirect_to']
                return redirect(redirect_to)
            else:
                mode = 'buyer' if user.mode == 'B' else "seller"
                return redirect(f"{mode}:dashboard")

    return render(request,'accounts/register.html', {
        'form': form
    })


def login(request):
    """
    REGISTER:
        GET CREATE USER FORM
        IF POST:
            GET USERNAME AND PASSWORD
            AUTHENTICATIE THE USERNAME AND PASSWORD
            IF USER FOUND: LOGGED IN THE USER AND REDIRECT TO DASHBOARD
            ELSE: RETURN THE INVALID USER FORM
                
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user= authenticate(request, username=username, password=password)

        if user is not None:
            dj_login(request, user)
            redirect_to = request.session.get('redirect_to', None) # IF REDIRECT URL: MARKETED CUSTOMER
            if redirect_to:
                del request.session['redirect_to']
                return redirect(redirect_to)
            else:
                mode = 'buyer' if user.mode == 'B' else "seller"
                return redirect(f"{mode}:dashboard")
        else:
            messages.info(request,'Username Or Password is incorrect')
    context={}
    return render(request,'accounts/login.html',context)


def logout(request):
    """
    LOGOUT USER
    """
    dj_logout(request)
    return redirect('core:index')


def user_profile(request):
    """
    IF LOGGED IN: RETURN TO PROFILE PAGE
    IF NOT LOGGED IN: RETURN ERROR
    """
    if request.user.is_authenticated:
        context={}
        return render(request, 'accounts/user_profile.html', context)
    else:
        return HttpResponse('please login with your credentials to view user profile page ')


def user_mode_switch(request):
    if request.method == 'POST':
        u = request.user
        if u.mode == 'S':
            u.mode = 'B'
        elif u.mode == 'B':
            u.mode = 'S'
        u.save()
        return redirect(f"{u.get_mode_display()}:dashboard")
