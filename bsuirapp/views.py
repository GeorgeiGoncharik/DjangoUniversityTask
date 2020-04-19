from django.http import HttpResponse
from django.shortcuts import render

def get_lol_page(request):
    return render(request, 'static/lolpage.html')