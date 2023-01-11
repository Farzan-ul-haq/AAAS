from django.shortcuts import render

# Create your views here.

def brochure_list(request):
    """Returns Brochure List"""
    return render(request, 'market/brochure-list.html')

def brochure_detail(request, pk):
    """Returns Brochure List"""
    return render(request, 'market/brochure-detail.html')
