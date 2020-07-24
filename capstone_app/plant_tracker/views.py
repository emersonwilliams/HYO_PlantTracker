from django.shortcuts import render
from . import test_login_method
# ...
from django.http import HttpResponse
import datetime
from django.views.decorators.csrf import csrf_exempt
from . import models

user_dict = {}
for obj in models.User.objects.all():
    user_dict[obj.user_name] = obj.passwd

# Create your views here.
@csrf_exempt
def home(request):
    return render(request, 'home.html', {})

@csrf_exempt
def login(request):
    if request.method == "POST":
        name = request.POST.get("username")
        password = request.POST.get("password")
        try:
            if user_dict[name] == password: return render(request, "myplants.html")
            else: raise KeyError
        except:
            return render(request, "login.html")

    return render(request, 'login.html', {})

@csrf_exempt
def register(request):
    return render(request, 'register.html', {})

@csrf_exempt
def myplants(request):
    return render(request, 'myplants.html', {})

def addplant(request):
    return render(request, 'addplant.html', {})

def plantdetail(request, plant_id):
    # Need to add stuff to handle actually getting and displaying the detail !
    return render(request, 'plantdetail.html', {})