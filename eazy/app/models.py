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
    sizes = models.ManyToManyField(Size, related_name='Sizes')
    quantity = models.PositiveIntegerField(default=0)  # New field for stock quantity

    def is_out_of_stock(self):
        return self.quantity <= 0

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
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Allows null values
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)  # Allows null values
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.customer_name} on {self.created_at}"







  
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username






