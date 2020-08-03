from django.shortcuts import render
# ...
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
import datetime
from django.views.decorators.csrf import csrf_exempt
from . import models, forms
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm

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

            auth_login(request, user)
            return redirect("myplants")

        else:
            message = "Login attempt failed. Please try again or register to create an account."
            return render(request, "test_login.html", {"error_message": message})

    return render(request, 'test_login.html')

@csrf_exempt
def register(request):
    form = forms.RegistrationForm()

    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            print("Saving user..")
            form.save()
            return redirect("login")

    context = {"form": form}
    return render(request, 'register.html', context)

@csrf_exempt
def myplants(request):
    return render(request, 'myplants.html', {})

def addplant(request):
    return render(request, 'addplant.html', {})

def plantdetail(request, plant_id):
    # Need to add stuff to handle actually getting and displaying the detail !
    return render(request, 'plantdetail.html', {})