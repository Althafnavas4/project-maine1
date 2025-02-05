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
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']
        confirm_password = req.POST['confirm_password']
        
        # Check if the passwords match
        if password != confirm_password:
            messages.warning(req, 'Passwords do not match.')
            return redirect(register)
        
        try:
            # Create the user if passwords match
            data = User.objects.create_user(first_name=name, email=email, password=password, username=email)
            data.save()
            
            # Success message
            messages.success(req, 'Account created successfully. You can now log in.')
            return redirect(eazy_login)
        except:
            messages.warning(req, 'User already exists.')
            return redirect(register)
    else:
        return render(req, 'user/register.html')





      
    
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


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Buy, Order

def booking(req):
    if req.method == "POST":
        # Process status updates from the admin page
        for key, value in req.POST.items():
            if key.startswith('status_'):  # Look for status fields
                buy_id = key.split('_')[1]  # Extract the Buy ID from the key
                try:
                    buy = Buy.objects.get(id=buy_id)
                    old_status = buy.status  # Capture the previous status
                    if old_status != value:  # Only update if the status is different
                        buy.status = value  # Update the status field
                        buy.save()  # Save the changes
                        messages.success(req, f"Order {buy_id} status updated from {old_status} to {value}.")
                    else:
                        messages.info(req, f"Order {buy_id} status is already {value}.")
                except Buy.DoesNotExist:
                    messages.error(req, f"Order {buy_id} not found.")
        
        return redirect('booking')  # Redirect to refresh the admin page

    # Display all orders and buys
    buys = Buy.objects.all().order_by('-date')  # Adjust to sort by the appropriate field
    orders = Order.objects.all().order_by('-created_at')  # Adjust to sort by the appropriate field

    combined_data = zip(buys, orders)

    return render(req, 'shop/booking.html', {'combined_data': combined_data, 'buys': buys, 'orders': orders})







    #------------------------user--------------------------------

def user_home3(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req, 'first.html', {'data': data, 'user': req.user})

    else:
        return redirect(eazy_login)

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
        product = get_object_or_404(Product, pk=pid)
        size_name = req.POST.get('size')
        size = get_object_or_404(Size, size=size_name)
        user = User.objects.get(username=req.session['user'])

        # Check if the product is already in the cart
        cart_item, created = Cart.objects.get_or_create(user=user, product=product, size=size)

        if not created:
            cart_item.quantity += 1  # Increment quantity if already in cart
        cart_item.save()

        messages.success(req, 'Product added to cart successfully.')
        return redirect(view_cart)
    return redirect('eazy_login')



# Update cart quantity and adjust the total price accordingly
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Cart

def update_cart_quantity(request, cart_id, action):
    cart_item = get_object_or_404(Cart, id=cart_id)

    # Get the price of the product
    item_price = cart_item.product.offer_price  # Assuming 'product' is a related field on Cart

    # Increase or decrease quantity and update total price
    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")
            return redirect('view_cart')

    # Update total price based on new quantity
    cart_item.total_price = cart_item.quantity * float(item_price)

    # Save the updated cart item
    cart_item.save(update_fields=['quantity', 'total_price'])  # Ensure the update is saved

    messages.success(request, f"Updated cart: {cart_item.product.name}, Quantity: {cart_item.quantity}")
    
    return redirect(view_cart)




# View the cart and calculate the total price dynamically based on quantity and product price
def view_cart(request):
    if 'user' in request.session:
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        # Calculate the total price based on quantity and individual item price
        total_price = sum(item.total_price for item in cart_items) if cart_items else 0

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

from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import User, Cart, Product, Size, Buy

def user_buy(req, pid):
    user = get_object_or_404(User, username=req.session.get('user'))
    
    # Fetch the updated cart item
    cart = get_object_or_404(Cart, pk=pid)
    
    size_name = req.POST.get('size')
    size = get_object_or_404(Size, size=size_name)
    product = cart.product
    quantity_to_buy = cart.quantity
    total_price = cart.total_price  

    with transaction.atomic():
        # Lock the product row to prevent race conditions
        product = Product.objects.select_for_update().get(pk=product.pk)

        if product.quantity < quantity_to_buy:
            messages.error(req, 'Sorry, this product is out of stock.')
            return redirect('view_cart')

        # Reduce stock
        product.quantity = F('quantity') - quantity_to_buy
        product.save(update_fields=['quantity'])

        # Filter all existing Buy entries for this user, product, and size
        existing_buy_entries = Buy.objects.filter(
            user=user,
            product=product,
            size=size
        )

        if existing_buy_entries.exists():
            # If Buy entries exist, update their quantity and price
            for entry in existing_buy_entries:
                entry.quantity += quantity_to_buy  # Add quantity
                entry.price += total_price  # Add total price
                entry.save(update_fields=['quantity', 'price'])
        else:
            # If no Buy entries exist, create a new one
            Buy.objects.create(
                user=user,
                product=product,
                price=total_price,
                size=size,
                quantity=quantity_to_buy
            )

        # Remove the cart item after successful purchase
        cart.delete()

    messages.success(req, f'Product "{product.name}" purchased successfully!')
    return redirect('order_page')






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

    enriched_buy = []
    for order in buy:
        enriched_buy.append({
            'product': order.product,
            'price': order.price,
            'size': order.size,
            'order_id': order.id,  # Ensure this is populated
            'status': order.status,
            'estimated_delivery': order.date + timezone.timedelta(days=5),
            'shipping_address': user.userprofile.address if hasattr(user, 'userprofile') and user.userprofile.address else 'No address provided',
            'email': user.email if user.email else 'No email provided',
            'phone_number': user.userprofile.phone_number if hasattr(user, 'userprofile') and user.userprofile.phone_number else 'No phone number provided',
        })

    return render(req, 'user/bookings.html', {'buy': enriched_buy})






def userprd(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/shop.html',{'data':data})
    else:
        return redirect(user_home)
    
from .forms import OrderForm

# views.py
from django.shortcuts import render, redirect
from .forms import OrderForm
from django.contrib import messages

def order_page(request):
    if request.user.is_authenticated:
        user = request.user  # Get logged-in user
        
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                # Process the order and save it
                order = form.save(commit=False)
                order.user = user  # Link order to the user
                order.save()
                messages.success(request, "Order placed successfully.")
                return redirect(order_success)  # Redirect to success page
        else:
            # Pre-fill form with user details
            form = OrderForm(initial={'user': user})
        
        return render(request, 'user/order.html', {'form': form})
    else:
        return redirect('login')  # Redirect to login page if not authenticated



   




def order_success(request):
    return render(request, 'user/order_success.html')



def user_orders_view(request):
    # Get all orders related to the user
    orders = Order.objects.all()  # Or you can filter it by the logged-in user: Order.objects.filter(user=request.user)
    
    # Get all the associated Buy data
    buys = Buy.objects.all()  # Or filter by user if needed: Buy.objects.filter(user=request.user)

    # Combine the data into a list of dictionaries or tuples
    combined_data = []
    for order in orders:
        # Get the corresponding buy instance
        buy = buys.filter(user=order.user, product=order.product).first()  # Ensure you filter by matching buy

        # Add combined data
        if buy:
            combined_data.append({
                'order': order,
                'buy': buy
            })

    return render(request, 'orders.html', {'combined_data': combined_data})







from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserProfileForm
from .models import UserProfile

def user_profile(request):
    user = request.user  # Get the logged-in user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)  # Create a profile if it doesn't exist

    # Check if the cancel button was clicked
    if request.GET.get('cancel'):
        messages.info(request, 'Profile update canceled.')  # Add cancel message
        return redirect('user_profile')  # Redirect to the profile page after canceling

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")  # Add success message
            return redirect('user_profile')  # Redirect to the profile page after saving
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'user/profile.html', {'form': form})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Buy

def cancel_order(request, pid):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to cancel an order.")
        return redirect('eazy_login')

    # Fetch the order
    buy = get_object_or_404(Buy, id=pid, user=request.user)

    # Ensure the user owns this order
    if buy.user != request.user:
        messages.error(request, "You are not authorized to cancel this order.")
        return redirect(user_booking)

    # Mark the order as canceled
    buy.status = 'Canceled'
    buy.save()

    messages.success(request, f"Order {pid} has been successfully canceled.")
    return redirect(user_booking)




from django.shortcuts import redirect
from django.contrib import messages

def clear_all_orders(request):
    if request.method == "POST":
        user = request.user
        Buy.objects.filter(user=user).delete()
        messages.success(request, "All orders have been cleared successfully.")
    return redirect(user_booking)



    



from django.shortcuts import redirect
from django.contrib import messages
from .models import Buy, Order

def clear_all_orders2(request):
    if request.method == "POST":
        # Ensure the user has admin privileges before clearing orders
        if request.user.is_staff:  # This check ensures only admins can clear orders
            # Delete all Buy and Order objects (for all users)
            Buy.objects.all().delete()  # Deletes all buy records for all users
            Order.objects.all().delete()  # Deletes all order records for all users
            
            messages.success(request, "All orders have been cleared successfully.")
        else:
            messages.error(request, "You do not have permission to clear all orders.")

    return redirect(booking)  # Redirect to admin booking page. Make sure this URL is correct.



   




from django.shortcuts import redirect
from .models import UserProfile

def shop_now(request):
    user = request.user

    try:
        profile = user.userprofile
        # Check if required fields are filled
        if profile.name and user.email and profile.address:  # Check user.email instead of profile.email
            return redirect(userprd)  # Redirect to user products page
        else:
            return redirect(user_profile)  # Redirect to profile page if incomplete
    except UserProfile.DoesNotExist:
        return redirect(user_profile)  # Redirect to profile if it doesn't exist
