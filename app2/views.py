from django.shortcuts import render, redirect
from app1.models import *
from django.contrib import messages
import datetime

def admin (request):
    return render(request, "admin.html")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/admin')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['id'] = user.id
        if user.admin == "Dojo":
            return redirect('/admin/dashboard/products')
        else:
            return redirect ('/dashboard/all')

def orders (request):
    if 'id' not in request.session:
        return redirect('/admin')
    else:
        context={
            'all_orders': Order.objects.all()
        }
        return render(request, ('orders.html'),context)

def products (request):
    if 'id' not in request.session:
        return redirect('/admin')
    else:
        product= Product.objects.all().values_list('image1', flat=True).distinct()
        listt=[]
        for p in product:
            listt.append(Product.objects.filter(image1=p).first()) 
        all_productz=Product.objects.all()
        product_dic={}
        for pro in all_productz:
            if pro.image1 in product_dic:
                product_dic[pro.image1]+=1
            else:
                product_dic[pro.image1]=1
        context={
            'all_products': listt,
            'product_count': product_dic
        }
        return render(request, ('products.html'),context)


def edit_form(request, num):
    if 'id' not in request.session:
        return redirect('/admin')
    else:
        context= {
            'product': Product.objects.get(id=num),
            }
        return render(request, "edit_product.html", context)

def delete(request, num):
    Product.objects.get(id=num).delete()
    return redirect('/admin/dashboard/products')  

def update_form(request, num):
    update_pr = Product.objects.get(id=num)
    products=Product.objects.all()
    list1=[]
    for p in products:
        if p.image1==update_pr.image1:
            print('yes')
            list1.append(Product.objects.get(id=p.id))
    for product in list1:
        product.name= request.POST['name']
        product.desc= request.POST['desc']
        product.price= request.POST['price']
        product.category= request.POST['category']
        product.image1= request.POST['image1']
        product.image2= request.POST['image2']
        product.image3= request.POST['image3']
        product.image4= request.POST['image4']
        product.save()
    return redirect('/admin/dashboard/products')  


def add(request):
    Product.objects.create(
        name=request.POST['name'],
        desc=request.POST['desc'],
        price=request.POST['price'],
        category=request.POST['category'],
        image1=request.POST['image1'],
        image2=request.POST['image2'],
        image3=request.POST['image3'],
        image4=request.POST['image4'],
        color=request.POST['color'],
        size=request.POST['size'],
        gender=request.POST['gender'],
    )
    return redirect('/admin/dashboard/products')

def add_product(request):
    if 'id' not in request.session:
        return redirect('/admin')
    else:
        return render(request,('add.html'))