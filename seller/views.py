from django.shortcuts import render, redirect
from django.http import Http404


PRODUCT_TYPES = ["API", 'LOGO', "TEMPLATE", "SOFTWARE"]

def seller_dashboard(request):
    return render(request, 'seller/dashboard.html')


def create_logo(request):
    if request.method == 'GET':
        return render(
            request,
            'seller/create-logo.html'
            )
    if request.method == 'POST':
        print('PRODUCT SUBMITTED')
        return redirect('seller:dashboard')


def create_template(request):
    if request.method == 'GET':
        return render(
            request,
            'seller/create-template.html'
            )
    if request.method == 'POST':
        print('PRODUCT SUBMITTED')
        return redirect('seller:dashboard')


def create_software(request):
    if request.method == 'GET':
        return render(
            request,
            'seller/create-software.html'
            )
    if request.method == 'POST':
        print('PRODUCT SUBMITTED')
        return redirect('seller:dashboard')


def create_api(request):
    if request.method == 'GET':
        return render(
            request,
            'seller/create-api.html'
            )
    if request.method == 'POST':
        print('PRODUCT SUBMITTED')
        return redirect('seller:dashboard')