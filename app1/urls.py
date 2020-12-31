from django.urls import path     
from . import views

urlpatterns = [
    path('',views.index),
    path('dashboard/all', views.dashboard),
    path('cart', views.cart),
    path('checkout', views.checkout),
    path('checkout2', views.checkout2),
    path('log_and_reg', views.log_and_reg),
    path('logout', views.logout),
    # redirect
    path('dashboard/men/shirts',views.shirts_men),
    path('dashboard/men/jackets', views.jackets_men),
    path('dashboard/men/jeans', views.jeans_men),

    path('dashboard/women/shirts',views.shirts_women),
    path('dashboard/women/jackets', views.jackets_women),
    path('dashboard/women/dresses', views.dresses_women),
    path('dashboard/women/jeans', views.jeans_women),

    path('detailes/<item_category>/<int:item_id>', views.detailes),
    path('add_to_cart',views.add_to_cart),
    path('register', views.register),
    path('logout',views.logout),
    path('login', views.login),

    path('success', views.success),
    path('remove_item/<int:item_id>', views.remove_item),
    path('view_success', views.view_success),
    path('create_order', views.create_order),
    path('favorit/<int:id>', views.favorit),
    path('unfavorit/<int:id>', views.unfavorit),
    path('cancel', views.cancel)

]