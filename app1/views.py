from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import datetime
import random
import os
import stripe
stripe.api_key = 'sk_test_51I3T3TLErIUdREr9TLwSIKIesvKpb5aDK1ZtkxA1HFeKqELlvlhnCebH5E5thNkIZhNN38CVpiuiI0xMrDepHBCm005npvMPiA'

def log_and_reg(request):
    return render(request,('index.html'))

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/log_and_reg')
    else:
        password = request.POST['password']
        hash_browns = bcrypt.hashpw(
        password.encode(), # pw to hash
        bcrypt.gensalt() # generated salt bae
        ).decode()  # create the hash
        if request.POST['admin']=='Dojo':
            user=User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hash_browns,
            admin=request.POST['admin']
        )
        else:
            user=User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hash_browns,
        )
        request.session['id']=user.id
        Cart.objects.create(product_for=User.objects.get(id=user.id))
        print("*********************************************************************************")
        print(Cart.objects.all())
        if 'total' not in request.session:      
            request.session['total']=0
        return redirect('/dashboard/all')

def logout(request):
    if 'id' in request.session:
        del request.session['id']
    return redirect('/dashboard/all')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/log_and_reg')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['id'] = user.id
        if 'total' not in request.session:
            request.session['total']=0
        return redirect('/dashboard/all')


def index(request):
    return redirect('/dashboard/all')

def cart(request):
    if 'id' not in request.session:
        return redirect('/log_and_reg')
    else:
        context={
            'cart':Cart.objects.get(product_for=User.objects.get(id=request.session['id']))
        }
        return render(request,('cart.html'),context)

def checkout(request):
    if 'id' not in request.session:
        return redirect('/log_and_reg')
    else:
        context={
            'cart':Cart.objects.get(product_for=User.objects.get(id=request.session['id'])),
            'this_user':User.objects.get(id=request.session['id'])
        }
        return render(request, ('checkout.html'), context)

def checkout2(request):
    errors = User.objects.billing_validator(request.POST)
    print("*"*20)
    print(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/checkout')
    if 'id' not in request.session:
        return redirect('/log_and_reg')
    if request.session['total']==0:
        return redirect('/checkout')
    user= User.objects.get(id=request.session['id'])
    user.address=request.POST['address']
    user.city=request.POST['city']
    user.street=request.POST['street']
    user.phone_number=request.POST['phone']
    user.save()
    return render(request, ('checkout1.html'))

def dashboard(request):
    # user=User.objects.get(id=request.session['id'])
    # user.admin="yes"
    # user.save()
    product= Product.objects.all().values_list('image1', flat=True).distinct()
    listt=[]
    for p in product:
        listt.append(Product.objects.filter(image1=p).first()) 
    context={
        'all_products': listt,
        'name':"All",
    }
    return render(request, ('dashboard.html'), context)

def shirts_men(request):
    context={
        'all_products':Product.objects.filter(category="shirts").filter(size="S").filter(gender="male"),
        'name':"Shirts"
    }
    return render(request, ('dashboard.html'), context)

def jackets_men(request):
    context={
        'all_products':Product.objects.filter(category="jackets").filter(size="S").filter(gender="male"),
        'name':"Jackets"
    }
    return render(request, ('dashboard.html'), context)

def jeans_men(request):
    context={
        'all_products':Product.objects.filter(category="jeans").filter(size="S").filter(gender="male"),
        'name':"Jeans"
    }
    return render(request, ('dashboard.html'), context)

def shirts_women(request):
    context={
        'all_products':Product.objects.filter(category="shirts").filter(size="S").filter(gender="female"),
        'name':"Shirts"
    }
    return render(request, ('dashboard.html'), context)

def jackets_women(request):
    context={
        'all_products':Product.objects.filter(category="jackets").filter(size="S").filter(gender="female"),
        'name':"Jackets"
    }
    return render(request, ('dashboard.html'), context)

def dresses_women(request):
    context={
        'all_products':Product.objects.filter(category="dresses").filter(size="S").filter(gender="female"),
        'name':"Dresses"
    }
    return render(request, ('dashboard.html'), context)

def jeans_women(request):
    context={
        'all_products':Product.objects.filter(category="jeans").filter(size="S").filter(gender="female"),
        'name':"Jeans"
    }
    return render(request, ('dashboard.html'), context)

def detailes(request,item_category,item_id):
    if 'id' not in request.session:
        return redirect('/log_and_reg')
    else:
        this_item=Product.objects.get(id=item_id)
        context={
            'item':this_item,
            'similar_items':Product.objects.exclude(id=item_id).filter(category=item_category).filter(size="S").filter(gender=this_item.gender),
            'sizes':Product.objects.filter(image1=this_item.image1),
            'user':User.objects.get(id=request.session['id']),        
        }
        return render(request,'item.html',context)


def add_to_cart(request):
    if 'id' not in request.session:
        return redirect('/log_and_reg')
    else:
        print(request.POST)
        user=User.objects.get(id=request.session['id'])
        cart=Cart.objects.get(product_for=user)
        print(cart)
        product=Product.objects.get(id=request.POST['size'])
        if product not in cart.product_item.all():
            cart.product_item.add(product)
            request.session['total']+=float(product.price)
        return redirect('/cart')

def remove_item(request, item_id):
    user=User.objects.get(id=request.session['id'])
    cart=Cart.objects.get(product_for=user)
    product=Product.objects.get(id=item_id)
    cart.product_item.remove(product)
    request.session['total']-=float(product.price)
    print(cart.product_item.all())
    return redirect('/cart')


def success(request):
    customer= stripe.Customer.create(
    email= request.POST['email'],
    name= request.POST['name'],
    source= request.POST['stripeToken']
    )
    stripe.Charge.create(
    customer=customer,
    amount=int(request.session['total'])*100,
    currency="usd",
    description= "Payment"
    )
    return redirect('/create_order')


def create_order(request):
    user= User.objects.get(id= request.session['id'])
    cart= Cart.objects.get(product_for=user)
    quantity=len(cart.product_item.all())
    Order.objects.create(
        order_number=random.randint(10000, 99999),
        ordered_by=user,
        quantity_ordered=quantity,
        total_price=request.session['total']
    )
    for product in cart.product_item.all():
        this= Product.objects.get(id= product.id)
        this.delete()
        request.session['total']=0
    return redirect('/view_success')


def view_success(request):
    order =Order.objects.last()
    context={
        'this_order': Order.objects.last(),
        'order_number': order.order_number
    }
    return render(request,('success.html'), context)

def favorit(request,id):
    product = Product.objects.get(id=id)
    user = User.objects.get(id=request.session['id'])
    user.likes.add(product)
    return redirect(f'/detailes/{product.category}/{id}')

def unfavorit(request,id):
    product = Product.objects.get(id=id)
    user = User.objects.get(id=request.session['id'])
    user.likes.remove(product)
    return redirect(f'/detailes/{product.category}/{id}')


def cancel(request):
    return redirect('/checkout')