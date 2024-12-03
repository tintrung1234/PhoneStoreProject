from django.db import models
from datetime import datetime
from django.contrib.auth.models import UserManager
# from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.conf import settings

# Create your models here.
class Role(models.Model):
    id= models.IntegerField(primary_key =True)
    name= models.CharField(max_length=255)

class Employee(models.Model):
    Roleid = models.ForeignKey('Role',on_delete=models.CASCADE)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    USERNAME_FIELD = models.CharField(max_length=255, unique=True)  # Change to 'username' for clarity
    fullName = models.CharField(max_length=255)
    birthDate = models.DateField()
    gender = models.BooleanField()
    password = models.CharField(max_length=255)
    verify_password = models.CharField(max_length=255, default=False)
    image = models.CharField(max_length=255)
    status = models.BooleanField()
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    last_login = models.DateTimeField(blank=True, null=True)

    @staticmethod
    def authenticate(username=None, password=None):
        if username is not None and password is not None:
            # Perform authentication based on username and password
            if username == settings.ADMIN_LOGIN:
                # Check password against settings
                if check_password(password, settings.ADMIN_PASSWORD):
                    # Try to get the user from the database
                    try:
                        user = User.objects.get(username=username)
                        return user
                    except User.DoesNotExist:
                        # If the user does not exist, create a new one
                        user = User.objects.create(username=username, is_staff=True, is_superuser=True)
                        return user
        return None
    

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.IntegerField()
    image = models.ImageField()
    updateDate = models.DateField()
    provider = models.CharField(max_length=255)
    catid = models.ForeignKey('Category', on_delete=models.CASCADE)

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    

class Category(models.Model):
    name = models.CharField(max_length=255)
    discription = models.CharField(max_length=255)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'