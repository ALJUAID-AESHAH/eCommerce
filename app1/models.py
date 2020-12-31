from django.db import models
import datetime
import bcrypt
import re
import random

class UserManager(models.Manager):
    def login_validator(self, post_data):
        errors = {}
        # check username in db
        email_list = User.objects.filter(email=post_data['email'])
        if len(email_list) == 0:    
            errors['email'] = 'There was a problem'
        # check password
        elif not bcrypt.checkpw(
            post_data['password'].encode(),  # from the form
            email_list[0].password.encode()  # from the db
        ):
            # errors['password'] = 'Password did not match'
            errors['password'] = 'There was a problem'
        return errors

    def register_validator(self, post_data):
        errors = {}
        # check username
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'first name must be longer than 2 characters'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'last name must be longer than 2 characters'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):           
            errors['email'] = "Invalid email address!"
        # check password
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be longer than 8 characters'
        if post_data['password'] != post_data['confirm']:
            errors['confirm'] = 'Password does not match'
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors['email'] = 'email taken'
        return errors

    def billing_validator(self, post_data):
        errors = {}
        if len(post_data['address']) < 2:
            errors['address'] = 'The address is too short!'
        if len(post_data['city']) < 2:
            errors['city'] = 'The city name is too short!'    
        if len(post_data['street']) < 2:
            errors['street'] = 'The street name is too short!'    
        if len(post_data['phone']) != 10:
            errors['phone'] = 'Phone number should be 10 digits long!'
        return errors

class User(models.Model):
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    address=models.TextField(null=True)
    city=models.CharField(max_length=255, null=True)
    street=models.CharField(max_length=255, null=True)
    zipcode=models.IntegerField(null=True)
    card=models.IntegerField(null=True)
    security_code=models.IntegerField(null=True)
    name_on_card=models.CharField(max_length=255, null=True)
    phone_number=models.IntegerField(null=True)
    exp= models.DateField(null=True)
    admin=models.CharField(max_length=3, null=True)
    objects=UserManager()



class Product(models.Model):
    name=models.CharField(max_length=255)
    desc=models.TextField()
    price=models.DecimalField(decimal_places=2, max_digits=5)
    category=models.CharField(max_length=255)
    image1=models.TextField()
    image2=models.TextField()
    image3=models.TextField()
    image4=models.TextField()
    color=models.CharField(max_length=45)
    size=models.CharField(max_length=1)
    gender=models.CharField(max_length=45)
    liked_by= models.ManyToManyField(User, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    order_number=models.IntegerField(null=True) 
    ordered_by=models.ForeignKey(
        User, related_name='orders', on_delete=models.CASCADE)
    quantity_ordered = models.IntegerField()
    total_price = models.DecimalField(decimal_places=2, max_digits=6)
    product_item= models.ManyToManyField(Product, related_name='product_in_order')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    product_for=models.ForeignKey(
    User, related_name='cart', on_delete=models.CASCADE)
    product_item= models.ManyToManyField(Product, related_name='product_in_cart')
