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
    quantity = models.PositiveIntegerField(default=1)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Automatically calculate the total price based on quantity
        self.total_price = self.quantity * float(self.product.offer_price)
        super(Cart, self).save(*args, **kwargs)  # Add quantity field
   
    # Quantity field


# Buy model
class Buy(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='Pending'
    )  # New field for tracking delivery status

    def __str__(self):
        return f"{self.product.name} ({self.status})"
    




from django.db import models

class Order(models.Model):
    customer_name = models.CharField(max_length=100)

    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Allows null values
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)  # Allows null values
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.customer_name} on {self.created_at}"




# app/models.py



# models.py

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)# Linking the profile to the User
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)  # New field for date of birth
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True, null=True)  # Gender field
   
    def __str__(self):
        return self.user.username

  





