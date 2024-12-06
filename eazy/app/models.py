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



   
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)


class Buy(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True) 



class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    email = models.EmailField()

    def __str__(self):
        return f"Order by {self.customer_name} for {self.product_name}"
        
    def __str__(self):
        return f"Order {self.id} - {self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"