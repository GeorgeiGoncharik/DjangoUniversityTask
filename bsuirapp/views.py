from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
    return render(request, 'homepage.html')


def contacts(request):
    # return render(request, 'contacts.html')
    return HttpResponse('<h1>Будет позже</h1>')