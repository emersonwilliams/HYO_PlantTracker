from django.shortcuts import render
# ...
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
import datetime
from django.views.decorators.csrf import csrf_exempt
from . import models, forms
from .tasks import send_sms_reminder
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
import django.core.exceptions as e
from apscheduler.schedulers.background import BackgroundScheduler


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
            id = user.id
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
    if request.user.is_authenticated:
        context = {"data":[]}

        for plant in models.JoinUserPlants.objects.filter(user = request.user):
            plant_data = models.Plants.objects.get(plant_id = plant.plant_id)
            context["data"].append(plant_data)

        return render(request, "myplants.html", context)

    return render(request, 'register.html', {})

@csrf_exempt
def addplant(request):
    if request.method == "GET":
        return render(request, 'addplant.html', {})
    else:
        #TODO: need to make more flexible... return all results and lets user select via combo box and if no results, then prompt them to add the plant manually, save it to plants table, save to join table
        plant_name = request.POST.get("common-name")
        try:
            #TODO: handle multiple responses from query via letting users select from a combo box. Much of this view may change...
            plant = models.Plants.objects.get(plant_name__contains = plant_name)
        except e.ObjectDoesNotExist:
            context={"message": "Sorry. Plant not found in database."}
            return render(request, "plantnotfound.html", context)

        user = request.user
        nickname = request.POST.get("nickname")
        watering = request.POST.get("watering")

        join_instance = models.JoinUserPlants(user = user, plant = plant, nickname = nickname, watering_freq = watering)
        join_instance.save()

        # get user info to schedule SMS reminder
        username = user.get_name()
        phonenum = user.get_phone()

        scheduler = BackgroundScheduler()
        scheduler.add_executor('processpool')
        scheduler.add_job(send_sms_reminder, 'interval', args=[username, nickname, phonenum], days=int(watering))

        try:
            scheduler.start()
            print("Scheduler started")
            return render(request, 'addplant.html', {})
        except:
            # This shouldn't happen because then the user wouldn't get notifications
            print("Scheduler failed to start")
            return render(request, 'addplant.html', {})

@csrf_exempt
def delete(request, plant_id):
    user = request.user
    plant = plant_id
    models.JoinUserPlants.objects.filter(user = user).filter(plant = models.Plants.objects.get(plant_id = plant)).delete()
    return redirect("myplants")

def plantdetail(request, plant_id):
    # Need to add stuff to handle actually getting and displaying the detail !
    return render(request, 'plantdetail.html', {})