from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField
# Create your models here.

#create customer Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=30, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

#Create a User Profile when a user is created
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

#automate the profile thing
post_save.connect(create_profile, sender=User)

#Category of products
class Category(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

    #@daverobb2011
    class Meta:
        verbose_name_plural = 'categories' #verbose_name_plural

#Customers
class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = CloudinaryField('image', null=True, blank=True)
    #Add Sale Stuff
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True, null=True)
    def __str__(self):
        return self.name

#Customer orders
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

#sabbir : sabbir123
#jui : jui123