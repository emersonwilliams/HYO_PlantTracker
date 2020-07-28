from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    user_name = models.CharField(max_length=30)
    passwd = models.CharField(max_length=30)

    def __str__(self):
        return str(self.user_name) + str(self.passwd)
