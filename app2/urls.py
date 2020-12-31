from django.urls import path     
from . import views

urlpatterns = [
    path('',views.admin),
    path('add', views.add),
    path('login_admin', views.login),
    path('add_product', views.add_product),
    path('dashboard/orders',views.orders),
    path('dashboard/products',views.products),
    path('delete/<int:num>',views.delete),
    path('edit_form/edit/<int:num>', views.edit_form),
    path('update/<int:num>', views.update_form),
]   