from django.db import models

# Create your models here.


class Product(models.Model):
    ingredient = models.CharField(max_length=50)
