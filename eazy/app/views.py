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

from django.shortcuts import render
from .models import Buy, Order


from django.utils import timezone






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
    
    





from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.crypto import get_random_string

# Mock function to simulate email sending for verification
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'





# from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.conf import settings
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.utils.crypto import get_random_string

# # Mock function to simulate email sending for verification
# def send_verification_email(email, token):
#     subject = "Email Verification"
#     message = f"Click the link to verify your account: http://yourdomain.com/verify/{token}/"
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message, from_email, recipient_list)

# def register(req):
#     if req.method == 'POST':
#         name = req.POST['name']
#         email = req.POST['email']
#         password = req.POST['password']

#         # Password validation: at least 8 characters
#         if len(password) < 8:
#             messages.warning(req, 'Password must be at least 8 characters long.')
#             return redirect(register)

#         # Check if user already exists
#         if User.objects.filter(email=email).exists():
#             messages.warning(req, 'User already exists.')
#             return redirect(register)

#         try:
#             # Create user with inactive status
#             user = User.objects.create_user(
#                 first_name=name,
#                 email=email,
#                 password=password,
#                 username=email,
#                 is_active=False  # User is inactive until verified
#             )
#             user.save()

#             # Generate verification token
#             token = get_random_string(50)
#             # Save the token to the user profile or database (implement this)
#             # For example, user.profile.verification_token = token

#             # Send verification email
#             send_verification_email(email, token)

#             messages.success(req, 'Account created. Check your email for verification link.')
#             return redirect('eazy_login')
#         except Exception as e:
#             messages.error(req, f'Error: {str(e)}')
#             return redirect(register)
#     else:
#         return render(req, 'user/register.html')



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
            quantity = int(req.POST['quantity'])  # Fetch quantity from form

            product = Product.objects.create(
                pro_id=prd_id,
                name=prd_name,
                price=prd_price,
                offer_price=ofr_price,
                img=img,
                dis=dis,
                quantity=quantity  # Add quantity to the product
            )

            for size in sizes:
                size_obj, created = Size.objects.get_or_create(size=size)
                product.sizes.add(size_obj)

            return redirect(add_prod)
        else:
            all_sizes = Size.objects.all()
            return render(req, 'shop/add_prod.html', {'all_sizes': all_sizes})
    else:
        return redirect(eazy_login)

def edit(req, pid):
    if 'eazy' in req.session:
        if req.method == 'POST':
            prd_id = req.POST['prd_id']
            prd_name = req.POST['prd_name']
            prd_price = req.POST['prd_price']
            ofr_price = req.POST['ofr_price']
            dis = req.POST['dis']
            sizes = req.POST.getlist('sizes')  # Retrieve selected sizes
            img = req.FILES.get('img')  # Get the new image if uploaded
            quantity = req.POST['quantity']  # Retrieve quantity

            # Fetch the product to edit
            product = get_object_or_404(Product, pk=pid)

            # Update product fields
            product.pro_id = prd_id
            product.name = prd_name
            product.price = prd_price
            product.offer_price = ofr_price
            product.dis = dis
            product.quantity = quantity  # Update quantity

            # Update image if a new one is uploaded
            if img:
                product.img = img

            # Update sizes
            product.sizes.clear()  # Clear existing sizes
            for size in sizes:
                size_obj, _ = Size.objects.get_or_create(size=size)
                product.sizes.add(size_obj)

            product.save()  # Save all changes
            return redirect(home_ad)
        else:
            all_sizes = Size.objects.all()  # Fetch all available sizes
            product = get_object_or_404(Product, pk=pid)  # Fetch the product to edit
            return render(req, 'shop/edit.html', {'product': product, 'all_sizes': all_sizes})
    else:
        return redirect(eazy_login)


def delete(req,pid):
    data=Product.objects.get(pk=pid)
    url=data.img.url
    og_path=url.split('/')[-1]
    os.remove('media/'+og_path)
    data.delete()
    return redirect(home_ad)



def booking(req):
    buys = Buy.objects.all().order_by('-date')
    orders = Order.objects.all().order_by('-created_at')
    combined_data = zip(buys, orders)  # Pair the Buy and Order objects
    return render(req, 'shop/booking.html', {'combined_data': combined_data})




    #------------------------user--------------------------------



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
            size_name = req.POST.get('size')  # Get the selected size as a string
            size = get_object_or_404(Size, size=size_name)  # Fetch Size by its name
            user = User.objects.get(username=req.session['user'])

            # Create a new cart item with the selected size
            Cart.objects.create(user=user, product=product, size=size)
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


def user_buy(req, pid):
    # Get the user and cart details
    user = User.objects.get(username=req.session['user'])
    cart = Cart.objects.get(pk=pid)
    size_name = req.POST.get('size')  # Get the selected size
    size = get_object_or_404(Size, size=size_name)
    product = cart.product
    
    # Check if there's enough stock for the product
    if product.quantity > 0:
        # Reduce the quantity by 1 for the purchase
        product.quantity -= 1
        product.save()

        # Get the price from the cart's product offer price
        price = cart.product.offer_price

        # Create the purchase record
        buy = Buy.objects.create(user=user, product=product, price=price, size=size)
        buy.save()

        # Provide success message and redirect to order success page
        messages.success(req, 'Product purchased successfully!')
        return redirect('order_page')  # Ensure 'order_success' is a valid URL pattern
    else:
        # Handle out-of-stock case
        messages.error(req, 'Sorry, this product is out of stock.')
        return redirect('view_cart') 






def user_buy1(req, pid):
    # Get the user and product details
    user = User.objects.get(username=req.session['user'])
    product = Product.objects.get(pk=pid)
    size_name = req.POST.get('size')  # Get the selected size
    size = get_object_or_404(Size, size=size_name)

    # Check if the product is in stock
    if product.quantity > 0:
        # Deduct 1 from the stock
        product.quantity -= 1
        product.save()

        # Proceed to create the purchase record
        price = product.offer_price
        buy = Buy.objects.create(user=user, product=product, price=price, size=size)
        buy.save()

        messages.success(req, 'Product purchased successfully!')
        return redirect(order_page)
    else:
        # Handle the out-of-stock case
        messages.error(req, 'Sorry, this product is out of stock.')
        return redirect(view_cart)





                                            
                                            


def user_booking(req):
    user = User.objects.get(username=req.session['user'])
    buy = Buy.objects.filter(user=user).order_by('-date')
    orders = Order.objects.all().order_by('-created_at')

    enriched_buy = []
    for order in buy:
        enriched_buy.append({
            'product': order.product,
            'price': order.price,
            'size': order.size,
            'order_id': order.id,
            'status': 'Pending',
            'estimated_delivery': order.date + timezone.timedelta(days=5),
        })

    return render(req, 'user/bookings.html', {'buy': enriched_buy, 'orders': orders})


def userprd(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/shop.html',{'data':data})
    else:
        return redirect(user_home)
    
from .forms import OrderForm

def order_page(request):
    if 'user' in request.session:
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(order_success)  # Redirect to a success page
        else:
            form = OrderForm()
        return render(request, 'user/order.html', {'form': form})
    else:
        return redirect(eazy_login)



   



def order_success(request):
    return render(request, 'user/order_success.html')

