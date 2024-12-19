from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Product(models.Model):
    pro_id=models.TextField()
    name=models.TextField()
    price=models.IntegerField()
    offer_price=models.IntegerField()
    img=models.FileField()
    rating=models.TextField()
    dis=models.TextField()
   



   
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)


class Buy(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True) 




class Size(models.Model):
    prod = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    stock_quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.shoe.name} - Size {self.size}"



  