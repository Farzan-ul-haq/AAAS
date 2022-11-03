from django.shortcuts import render, HttpResponse , redirect
#from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from .forms import createuserform
from django.contrib import messages
from django.contrib.auth import authenticate, logout as dj_logout, login as dj_login
from django.contrib.auth.decorators import login_required
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
            messages.success(request,' Account Created ')
            dj_login(request, user)
            return redirect('base')
    context={'form':form}
    return render(request,'account/register.html',context)

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user= authenticate(request, username=username, password=password)
        
        if user is not None:
            dj_login(request, user)
            return redirect('base')
        else:
            messages.info(request,'Username Or Password is incorrect')
    context={}
    return render(request,'account/login.html',context)

def logout(request):
    dj_logout(request)
    return redirect('login')    

