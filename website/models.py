from django.db import models
from datetime import date

# Create your models here.

class Drug(models.Model):

    drug_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_purchased = models.IntegerField()
    expire_date = models.DateField()
    date_purchased = models.DateField(auto_now_add=True)



class Order(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    supplier_name = models.CharField(max_length=100)
    supplier_address = models.TextField()
    supplier_phone_number = models.IntegerField(max_length=20)
    date_ordered = models.DateField()

class Record(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_address = models.TextField()
    customer_phone_number = models.CharField(max_length=20)
    #drug_name = models.ForeignKey(Drug, on_delete=models.CASCADE )
    drug_name = models.CharField(max_length=255,choices=[(drug.drug_name, drug.drug_name) for drug in Drug.objects.all()])
    quantity_sold = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_sold = models.DateField(auto_now_add=True)



