from django.db import models
from django.contrib.auth.models import User

# Size model
class Size(models.Model):
    size = models.CharField(max_length=10)  # E.g., '6', '7', '8.5', '9', '10'

    def __str__(self):
        return self.size

# Product model
class Product(models.Model):
    pro_id = models.TextField()
    name = models.TextField()
    price = models.IntegerField()
    offer_price = models.IntegerField()
    img = models.FileField()
    rating = models.TextField()
    dis = models.TextField()
    sizes = models.ManyToManyField(Size, related_name='Sizes')  # Add sizes field

    def __str__(self):
        return self.name

# Cart model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

# Buy model
class Buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    


from django.db import models

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.customer_name} on {self.created_at}"





  