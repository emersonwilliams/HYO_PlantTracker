from django.shortcuts import render
# ...
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
import datetime
from django.views.decorators.csrf import csrf_exempt
from . import models

@csrf_exempt
def home(request):
    return render(request, 'home.html', {})

@csrf_exempt
def login(request):
    if request.method == "POST":
        #Authenticate is a Django implemented function. It takes credentials as keyword args, and checks for them in the auth_user table. If it verifies
        #the credentials, then it returns a user object, but returns false otherwise.
        user = authenticate(username=request.POST.get("username"), password = request.POST.get("password"))
        if user is not None:
            #Login is an additional function pre-implemented in Django. The function will store the user objects ID in a session, and I'm hoping it binds a
            #digital signature to the request object for stronger security but I think it just uses a cookie via a sessions table
            login(request, user)
            return render(request, "myplants.html")
        else:
            message = "Login attempt failed. Please try again or register to create an account."
            return render(request, "login.html", {"error_message": message})

    return render(request, 'login.html')

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