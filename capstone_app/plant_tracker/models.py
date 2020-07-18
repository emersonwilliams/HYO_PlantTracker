from django.db import models

# Create your models here.
class Example(models.Model):
    rand_attr = models.CharField(max_length=12)
