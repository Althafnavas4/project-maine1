from django.urls import path
from . import views
urlpatterns=[
    path('',views.eazy_login),
    path('eazy_logout',views.eazy_logout),

    # ----------------admin--------------------
    path('home_ad',views.home_ad),
   
    path('add_prod',views.add_prod),
    path('edit/<pid>',views.edit),
    path('delete/<pid>',views.delete),







    # --------------user---------------------


    path('register',views.register),
    path('user_home',views.user_home),
    path('view_pro/<pid>',views.view_pro),
]