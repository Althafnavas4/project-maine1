from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import *
from django.contrib import messages
from django.http import HttpResponse
from .models import Product
from .forms import CustomPasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView

from django.contrib.auth.forms import AuthenticationForm

from .forms import LoginForm, CustomPasswordResetForm









# Create your views here.

def eazy_login(req):
    if 'eazy' in req.session:
        return redirect(home_ad)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['passwd']
        data=authenticate(username=uname,password=password)
        
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['eazy']=uname   #create session
                return redirect(home_ad)
            else:
                
                login(req,data)
                req.session['user']=uname   #create session
                return redirect(user_home)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(eazy_login)
    else:
        return render(req,'login.html')
    
    
        
      
    
def home_ad(req):
    if 'eazy' in req.session:
        data=Product.objects.all()
        return render(req,'shop/home.html',{'data':data})
    else:
        return redirect(eazy_login)
    
def eazy_logout(req):
    req.session.flush()          #delete session
    logout(req)
    return redirect(eazy_login)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    form_class = CustomPasswordResetForm

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

def add_prod(req):
    if 'eazy' in req.session:
        if req.method == 'POST':
            prd_id = req.POST['prd_id']
            prd_name = req.POST['prd_name']
            prd_price = req.POST['prd_price']
            ofr_price = req.POST['ofr_price']
            dis = req.POST['dis']
            img = req.FILES['img']
            sizes = req.POST.getlist('sizes')

            product = Product.objects.create(
                pro_id=prd_id,
                name=prd_name,
                price=prd_price,
                offer_price=ofr_price,
                img=img,
                dis=dis
            )

            # Associate selected sizes
            for size in sizes:
                size_obj, created = Size.objects.get_or_create(size=size)
                product.sizes.add(size_obj)

            return redirect(add_prod)
        else:
            all_sizes = Size.objects.all()
            return render(req, 'shop/add_prod.html', {'all_sizes': all_sizes})
    else:
        return redirect(eazy_login)
    
def edit(req,pid):
    if 'eazy' in req.session:
        if req.method=='POST':
            prd_id=req.POST['prd_id']
            prd_name=req.POST['prd_name']
            prd_price=req.POST['prd_price']
            ofr_price=req.POST['ofr_price']
            dis=req.POST['dis']

            
            img=req.FILES.get('img')
            if img:
                Product.objects.filter(pk=pid).update(pro_id=prd_id,name=prd_name,price=prd_price,offer_price=ofr_price,dis=dis)
                data=Product.objects.get(pk=pid)
                data.img=img
                data.save()
            else:
                Product.objects.filter(pk=pid).update(pro_id=prd_id,name=prd_name,price=prd_price,offer_price=ofr_price,dis=dis)
            return redirect(home_ad)
        else:
            data=Product.objects.get(pk=pid)
            return render(req,'shop/edit.html',{'product':data})
    else:
        return redirect(eazy_login)

def delete(req,pid):
    data=Product.objects.get(pk=pid)
    url=data.img.url
    og_path=url.split('/')[-1]
    os.remove('media/'+og_path)
    data.delete()
    return redirect(home_ad)

def booking (req):
    buy=Buy.objects.all()[::-1] 
    return render (req,'shop/booking.html',{'buy':buy})


    #------------------------user--------------------------------

def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        # send_mail('user registration','eshop account created', settings.EMAIL_HOST_USER, [email])
        try:
           
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            return redirect(eazy_login)
        except:
            messages.warning(req,'User already exists.')
            return redirect(register)
    else:
        return render(req,'user/register.html')

def user_home(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/home.html',{'data':data})
    else:
        return redirect(eazy_login)
    
def view_pro(req, pid):
    product = get_object_or_404(Product, pk=pid)
    if 'user' in req.session:
        return render(req, 'user/view_pro.html', {'data': product, 'sizes': product.sizes.all(), 'show_sizes': True})
    else:
        return render(req, 'user/view_pro.html', {'data': product, 'sizes': product.sizes.all(), 'show_sizes': False})


        



def add_to_cart(req, pid):
    if 'user' in req.session:
        if req.method == 'POST':
            product = get_object_or_404(Product, pk=pid)
            Size = req.POST.get('size')  # Get the selected size as a string
            user = User.objects.get(username=req.session['user'])
            
            # Create a new cart item with the selected size
            Cart.objects.create(user=user, product=product, size=Size)
            messages.success(req, 'Product added to cart successfully.')
        return redirect(view_cart)
    return redirect('eazy_login')


def view_cart(request):
    if 'user' in request.session:
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        total_price = sum(float(item.product.offer_price) for item in cart_items) if cart_items else 0
        return render(request, 'user/cart.html', {'cart_items': cart_items, 'total_price': total_price})
    else:
        return redirect('eazy_login')



def delete_cart(request, id):
    if 'user' in request.session:
        cart_item = get_object_or_404(Cart, pk=id)
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
        return redirect(view_cart)
    else:
        return redirect('eazy_login')

def user_buy(request, id):
    if 'user' in request.session:
        cart_item = get_object_or_404(Cart, pk=id)
        user = request.user
        product = cart_item.product
        size = cart_item.size
        price = product.offer_price

        # Create a purchase record
        Buy.objects.create(user=user, product=product, size=size, price=price)
        cart_item.delete()  # Remove the item from the cart after purchase
        messages.success(request, 'Purchase successful!')
        return redirect('view_cart')
    else:
        return redirect('eazy_login')
def user_buy1(req, pid):
    if 'user' in req.session:
        if req.method == 'POST':
            product = get_object_or_404(Product, pk=pid)
            size_id = req.POST.get('size')
            size = get_object_or_404(Size, pk=size_id)
            user = User.objects.get(username=req.session['user'])
            Buy.objects.create(user=user, product=product, size=size, price=product.offer_price)
            messages.success(req, 'Purchase successful.')
        return redirect('order_success')
    return redirect('eazy_login')




                                            
                                            
def user_booking(req):
    user=User.objects.get(username=req.session['user'])
    buy=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/bookings.html',{'buy':buy})

def userprd(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/shop.html',{'data':data})
    else:
        return redirect(user_home)
    



   



def order_success(request):
    return render(request, 'user/order_success.html')

