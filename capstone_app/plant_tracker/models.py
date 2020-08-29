from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.backends.mysql.base import DatabaseWrapper
from datetime import datetime, timedelta
# Create your models here.
"""
08/03/2020
I need to:
1) extend auth.users to include phone number
2) decide on how to get/post plant data to the user_plants table
3) I also want to test in the template whether or not I'm grabbing the key 
    or the value from the context..
"""
DatabaseWrapper.data_types['DateTimeField'] = 'datetime'

class UserManager(BaseUserManager):
    def create_user(self, email, phone, password, full_name = None, active = True, admin = False):
        if not email or phone or password:
            raise ValueError("Must include required fields")
        new_user = self.model(
            email = self.normalize_email(email),
        )
        new_user.set_password(password) #also used to change password
        new_user.phone = phone
        new_user.full_name = full_name
        new_user.active = active
        new_user.admin = admin
        new_user.save()
        return new_user

    def create_admin(self, email, phone, password, full_name = None):
        new_user = self.create_user(email = email,
                         phone = phone,
                         password = password,
                         full_name = full_name,
                         active = True,
                         admin = True)
        return new_user

class CustomUser(AbstractBaseUser):
    #id, password, and lastlogin fields are inherited from abstractbaseuser
    email = models.EmailField(max_length=255, unique= True, default=None)
    full_name = models.CharField(max_length=255, blank=True, null=True, default=None)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=12, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)

    sched = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["phone", "full_name", "password"]

    objects = UserManager()

    def __str__(self):
        return (self.email, self.password)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.full_name
    
    def get_phone(self):
        return self.phone

    @property
    def length_of_account(self):
        return self.created

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

class Plants(models.Model):
    plant_id = models.AutoField(primary_key=True)
    plant_name = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=512, null=True)
    origin = models.CharField(max_length=512, null=True)
    growth_desc = models.CharField(max_length=512, null=True)
    poisonous_desc = models.CharField(max_length=512, null=True)
    light_desc = models.CharField(max_length=1000, null=True)
    watering_desc = models.CharField(max_length=1000, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.plant_name) + " " +str(self.date_added) + "\n" + \
               "Available Fields: plant_id, plant_name, image_url, scientific_name, origin, growth_desc, poisonous_desc, light_desc, watering_desc, date_added"

    #class Meta:
        #unique_together = ["plant_name", "origin"]


class JoinUserPlants(models.Model):
    combo_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    plant = models.ForeignKey(Plants, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    watering_freq = models.IntegerField(default=3)
    last_cared_for = models.DateTimeField(default=datetime.now)
    
    sched = None

    @property
    def next_water(self):
        #this function takes the current data and subtracts the amount of days specified in watering frequency, and then checks to see
        #if its been too many days since we last cared for the plant
        if datetime.now - timedelta(days=self.watering_freq) >= self.last_cared_for:
            #returning True could trigger the SMS system
            return True

    def get_plant_id(self):
        return self.plant

    def set_sched(self, scheduler):
        #print("set sched")
        self.sched = scheduler
    
    def get_sched(self):
        return self.sched

    def __str__(self):
        return self.nickname
        #return (self.user, self.plant, self.nickname)







