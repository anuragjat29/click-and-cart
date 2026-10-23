from tkinter.constants import CASCADE

from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

#Create your models here.
class product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=30)
    category= models.CharField(max_length=50,default="0")
    subcategory= models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    product_desc=models.CharField(max_length=300)
    Publ_date=models.DateField()
    image=models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.product_name

class contact(models.Model):
    message=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    gmail= models.CharField(max_length=50)
    phone= models.CharField(max_length=10)
    text=models.CharField(max_length=300)


    def __str__(self):
        return self.name

class orders(models.Model):
      user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True, related_name="orders")
      razorpay_order_id = models.CharField(default="")
      orders_id = models.AutoField(primary_key=True)
      name = models.CharField(max_length=30)
      gmail = models.CharField(max_length=50)
      amount = models.CharField(max_length=50,default="")
      address1 = models.CharField(max_length=100)
      address2 = models.CharField(max_length=100,blank=True)
      city = models.CharField(max_length=30)
      state = models.CharField(max_length=30)
      zip_code = models.CharField(max_length=10)
      phone = models.CharField(max_length=15)
      status = models.CharField(max_length=30, default="Placed")

class orderitems(models.Model):
    order = models.ForeignKey(orders, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    price = models.IntegerField()
    qty = models.IntegerField()

class orderupdate(models.Model):
    order = models.ForeignKey(orders, on_delete=models.CASCADE)
    order_desc = models.CharField(max_length=30)
    timestamp = models.DateTimeField(default=now)