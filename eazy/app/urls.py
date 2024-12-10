from django.urls import path
from . import views
from .views import  CustomPasswordResetView, CustomPasswordResetDoneView
urlpatterns=[
    path('',views.eazy_login),
    path('eazy_logout',views.eazy_logout),

    # ----------------admin--------------------
    path('home_ad',views.home_ad),
   
    path('add_prod',views.add_prod),
    path('edit/<pid>',views.edit),
    path('delete/<pid>',views.delete),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    
    path('password_reset_done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),







    # --------------user---------------------


    path('register',views.register),
    path('user_home',views.user_home),
    path('view_pro/<pid>',views.view_pro),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart),
    path('delete_cart/<id>',views.delete_cart),
    path('user_buy/<cid>',views.user_buy),
    path('user_buy1/<pid>',views.user_buy1),
    path('booking',views.booking),
    path('user_booking',views.user_booking),
    path('userprd',views.userprd),
    
    path('order_success/', views.order_success, name='order_success'),
    
]