from django.db import models
from django.core.validators import RegexValidator

class Organization(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10, unique=True, validators=[RegexValidator(r'^\d{10}$', message='Phone number must be 10 digits.')])
    website = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=50)
    password = models.CharField(max_length=100) 

class Products(models.Model):
    disease_name = models.CharField(max_length=100)
    product = models.CharField(max_length=250)
    product_link = models.CharField(max_length=1000)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)