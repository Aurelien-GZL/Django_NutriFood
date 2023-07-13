from django.db import models

# Create your models here.


class Product(models.Model):
    _DATABASE = 'default'
    id = models.CharField(max_length=13, primary_key=True)
    category = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    nutriscore_grade = models.CharField(max_length=1)
    nutriscore_score = models.SmallIntegerField(blank=True, null=True)
    product_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'product'
