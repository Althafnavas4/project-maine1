from django.urls import path
from .views import update_cart_quantity
from . import views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

urlpatterns=[

    path('', views.user_home3, name='user_home3'),
    path('login', views.eazy_login, name='eazy_login'),
    path('eazy_logout',views.eazy_logout, name='eazy_logout'),
    path("confirm_logout/", views.confirm_logout, name="confirm_logout"),

    # ----------------admin--------------------
    path('home_ad',views.home_ad, name='home_ad'),
   
    path('add_prod',views.add_prod),
    path('edit/<pid>',views.edit),
    path('delete/<pid>',views.delete),
    

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('admin/booking/', views.booking, name='booking'),

    # --------------user---------------------

    
    path('register/', views.register, name='register'),
    path('user_home',views.user_home),
    path('view_pro/<pid>',views.view_pro),
    path('add_to_cart/<pid>',views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('delete-cart/<int:id>',views.delete_cart, name='delete_cart'),
    path('user_buy/<int:pid>/', views.user_buy, name='user_buy'),

    path('user_buy1/<pid>',views.user_buy1, name='user_buy1'),
    path('booking',views.booking, name='booking'),
    path('user_booking',views.user_booking, name='user_booking'),
    path('userprd',views.userprd,  name='userprd'),
    path('order/', views.order_page, name='order_page'),
    path('order_success/',views.order_success, name='order_success'),
    path('profile/', views.user_profile, name='user_profile'),
    path('order/cancel/<int:pid>/', views.cancel_order, name='cancel_order'),
  
    path('update-cart/<int:cart_id>/<str:action>/', update_cart_quantity, name='update_cart_quantity'),
    path('clear_all_orders2', views.clear_all_orders2, name='clear_all_orders2'),
    path('shop-now/', views.shop_now, name='shop_now'),
    path('buy-all/', views.buy_all, name='buy_all'),
    path('create-order/<int:buy_id>/', views.create_order, name='create_order'),
    path('create_order2/<int:buy_id>/', views.create_razorpay_order, name="create_razorpay_order"),
    path('payment_success/', views.payment_success, name="payment_success"),
    path('verify_otp_reg',views.verify_otp_reg, name='verify_otp_reg')
    
]