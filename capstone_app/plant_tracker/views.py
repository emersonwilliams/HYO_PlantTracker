from django.shortcuts import render

# ...
from django.http import HttpResponse
import datetime

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def login(request):
    return render(request, 'login.html', {})
    
def register(request):
    return render(request, 'register.html', {})

def myplants(request):
    return render(request, 'myplants.html', {})

def addplant(request):
    return render(request, 'addplant.html', {})

def plantdetail(request, plant_id):
    # Need to add stuff to handle actually getting and displaying the detail !
    return render(request, 'plantdetail.html', {})