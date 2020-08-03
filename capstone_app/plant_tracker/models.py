from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.backends.mysql.base import DatabaseWrapper
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["phone", "full_name", "password"]

    objects = UserManager()

    def __str__(self):
        return (self.email, self.password)

    def get_name(self):
        return self.full_name
    @property
    def length_of_account(self):
        return self.created

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active



