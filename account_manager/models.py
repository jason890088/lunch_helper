from django.db import models


# Create your models here.
class Person(models.Model):
    line_user_id = models.CharField(max_length=50, unique=True)
    employee_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=15)
    corporation = models.CharField(max_length=30, unique=True)
