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




from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def register(req):
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']
        confirm_password = req.POST['confirm_password']

        # Check if the password is at least 8 characters long
        if len(password) < 8:
            messages.warning(req, 'Password must be at least 8 characters long.')
            return redirect(register)

        # Check if the passwords match
        if password != confirm_password:
            messages.warning(req, 'Passwords do not match.')
            return redirect(register)

        try:
            # Create the user if all conditions are met
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



def register(req):
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        password = req.POST['password']
        if User.objects.filter(email=email).exists():
            messages.warning(req, "Email already registered")
            return redirect('register')
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        req.session['email'] = email
        req.session['name'] = name
        req.session['password'] = password
        send_mail(
            'Your OTP Code',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER, [email]
        )
        messages.success(req, "OTP sent to your email")
        return redirect('verify_otp_reg')
    return render(req, 'user/register.html')

def verify_otp_reg(req):
    if req.method == 'POST':
        entered_otp = req.POST['otp'] 
        stored_otp = req.session.get('otp')
        email = req.session.get('email')
        name = req.session.get('name')
        password = req.session.get('password')
        if entered_otp == stored_otp:
            user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
            user.is_verified = True
            user.save()      
            messages.success(req, "Registration successful! You can now log in.")
            send_mail('User Registration Succesfull', 'Account Created Succesfully And Welcome To eazy', settings.EMAIL_HOST_USER, [email])
            return redirect(eazy_login)
        else:
            messages.warning(req, "Invalid OTP. Try again.")
            return redirect('verify_otp_reg')

    return render(req, 'verify.html')


      
    
from django.shortcuts import render, redirect
from .models import Product, ProductSize

def home_ad(req):
    if 'eazy' in req.session:
        data = Product.objects.all()

        # Create a list of tuples (product, size, quantity)
        product_size_list = []

        for product in data:
            product_sizes = ProductSize.objects.filter(product=product, quantity__gt=0)  # Only sizes with stock
            for ps in product_sizes:
                product_size_list.append((product, ps.size.size, ps.quantity))  # Store only available sizes

        return render(req, 'shop/home.html', {
            'data': data,
            'product_size_list': product_size_list  # Send as a list
        })
    else:
        return redirect(eazy_login)



    
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect

def confirm_logout(request):
    """ Renders a logout confirmation page """
    return render(request, "user/confirm_logout.html")  # Create this template

def eazy_logout(request):
    """ Logs out the user after confirmation """
    if request.method == "POST":
        request.session.flush()  # Delete session
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect("eazy_login")  # Redirect to login page
    return redirect("confirm_logout")  # If GET request, redirect to confirmation page





from django.shortcuts import render, redirect
from .models import Product, Size, ProductSize

def add_prod(req):
    if 'eazy' in req.session:
        if req.method == 'POST':
            prd_id = req.POST['prd_id']
            prd_name = req.POST['prd_name']
            prd_price = req.POST['prd_price']
            ofr_price = req.POST['ofr_price']
            dis = req.POST['dis']
            img = req.FILES['img']

            sizes = req.POST.getlist('sizes')  # List of selected sizes
            quantities = req.POST.getlist('quantities')  # List of corresponding quantities

            total_quantity = sum(map(int, quantities))  # Sum of all size-based stock

            # Create product
            product = Product.objects.create(
                pro_id=prd_id,
                name=prd_name,
                price=prd_price,
                offer_price=ofr_price,
                img=img,
                dis=dis,
                quantity=total_quantity
            )

            # Assign sizes and track quantity per size using ProductSize
            for size, qty in zip(sizes, quantities):
                size_obj, _ = Size.objects.get_or_create(size=size)
                ProductSize.objects.create(product=product, size=size_obj, quantity=int(qty))  # Store quantity per size

            return redirect(add_prod)
        else:
            all_sizes = Size.objects.all()

            # Initialize size-quantity list with default quantity 0
            size_quantity_list = [(size, 0) for size in all_sizes]

            return render(req, 'shop/add_prod.html', {
                'size_quantity_list': size_quantity_list
            })
    else:
        return redirect(eazy_login)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Size, ProductSize

def edit(req, pid):
    if 'eazy' in req.session:
        product = get_object_or_404(Product, pk=pid)

        if req.method == 'POST':
            prd_name = req.POST.get('prd_name', product.name)
            prd_price = req.POST.get('prd_price', product.price)
            ofr_price = req.POST.get('ofr_price', product.offer_price)
            dis = req.POST.get('dis', product.dis)
            img = req.FILES.get('img')

            sizes = req.POST.getlist('sizes')  # List of selected sizes
            quantities = req.POST.getlist('quantities')  # List of corresponding quantities

            # Update product fields
            product.name = prd_name
            product.price = prd_price
            product.offer_price = ofr_price
            product.dis = dis

            if img:
                product.img = img

            # Clear old size-quantity relationships
            ProductSize.objects.filter(product=product).delete()
            total_quantity = 0  # Track total stock

            for size, qty in zip(sizes, quantities):
                size_obj, _ = Size.objects.get_or_create(size=size)
                ProductSize.objects.create(product=product, size=size_obj, quantity=int(qty))  # Store quantity per size
                total_quantity += int(qty)

            product.quantity = total_quantity  # Update total stock
            product.save()

            return redirect(home_ad)

        else:
            all_sizes = Size.objects.all()

            # Fetch existing size quantities correctly
            size_quantity_list = [(ps.size.size, ps.quantity) for ps in ProductSize.objects.filter(product=product)]

            return render(req, 'shop/edit.html', {
                'product': product,
                'all_sizes': all_sizes,
                'size_quantity_list': size_quantity_list
            })
    else:
        return redirect(eazy_login)





def delete(req,pid):
    data=Product.objects.get(pk=pid)
    url=data.img.url
    og_path=url.split('/')[-1]
    os.remove('media/'+og_path)
    data.delete()
    return redirect(home_ad)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Buy, Order, UserProfile

def booking(req):
    if req.method == "POST":
        for key, value in req.POST.items():
            if key.startswith('status_'):
                buy_id = key.split('_')[1]
                try:
                    buy = Buy.objects.get(id=buy_id)
                    if buy.status != value:
                        buy.status = value
                        buy.save()

                        # ✅ Automatically delete "Canceled" orders from the database
                        if value == "Canceled":
                            buy.delete()
                            messages.warning(req, f"Order {buy_id} has been canceled and removed.")
                        else:
                            messages.success(req, f"Order {buy_id} status updated to {value}.")
                    else:
                        messages.info(req, f"Order {buy_id} status is already {value}.")
                except Buy.DoesNotExist:
                    messages.error(req, f"Order {buy_id} not found.")
        return redirect('booking')

    # ✅ Fetch only "Paid" orders
    buys = Buy.objects.filter(payment_status="Paid").order_by('-date')  

    combined_data = []
    for buy in buys:
        order = Order.objects.filter(buy=buy).first()

        # ✅ Fetch the user profile safely
        profile = getattr(buy.user, 'userprofile', None)

        # ✅ Ensure the correct customer name is displayed
        customer_name = profile.name if profile and profile.name else "N/A"

        if not order:
            order = Order.objects.create(
                buy=buy,
                customer_name=customer_name,  
                phone_number=profile.phone_number if profile and profile.phone_number else "N/A",
                email=buy.user.email if buy.user.email else "N/A",
                address=profile.address if profile and profile.address else "N/A",
            )

        combined_data.append({'buy': buy, 'order': order})

    return render(req, 'shop/booking.html', {'combined_data': combined_data})




from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Buy, Order, UserProfile

def create_order(request, buy_id):
    buy = get_object_or_404(Buy, id=buy_id)

    # ✅ Fetch the user profile safely
    profile = getattr(buy.user, 'userprofile', None)

    # ✅ Ensure an order doesn't already exist
    order, created = Order.objects.get_or_create(
        buy=buy,
        defaults={
            'customer_name': profile.name if profile and profile.name else "N/A",  # ✅ Corrected syntax
            'phone_number': profile.phone_number if profile and profile.phone_number else "",
            'email': buy.user.email if buy.user.email else "N/A",
            'address': profile.address if profile and profile.address else "",
        }
    )

    if created:
        messages.success(request, f"Order for {buy.product.name} created successfully!")
    else:
        messages.info(request, f"An order already exists for {buy.product.name}. No duplicate created.")

    return redirect('booking')





    #------------------------user--------------------------------

from django.shortcuts import render
from .models import Product

def user_home3(req):
    data = Product.objects.all()  # Get all products from the database
    return render(req, 'first.html', {'data': data, 'user': req.user})  # Render the page for all users


def user_home(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/home.html',{'data':data})
    else:
        return redirect(eazy_login)
    
from django.shortcuts import render, get_object_or_404
from .models import Product, ProductSize  # Ensure ProductSize is imported

def view_pro(req, pid):
    product = get_object_or_404(Product, pk=pid)
    
    # Fetch all sizes with their respective quantities for this product
    product_size_list = ProductSize.objects.filter(product=product)

    # Convert ProductSize objects into a list of tuples (size, quantity)
    size_quantity_list = [(ps.size.size, ps.quantity) for ps in product_size_list]

    return render(req, 'user/view_pro.html', {
        'data': product,
        'size_quantity_list': size_quantity_list,  # Send the size list
        'show_sizes': 'user' in req.session  # Check user session
    })

def add_to_cart(req, pid):
    if 'user' in req.session:
        product = get_object_or_404(Product, pk=pid)
        size_name = req.POST.get('size')

        if not size_name:
            messages.error(req, "Please select a size.")
            return redirect('view_pro', pid=pid)

        size = get_object_or_404(Size, size=size_name)
        user = User.objects.get(username=req.session['user'])

        # Check if the product is already in the cart
        cart_item, created = Cart.objects.get_or_create(user=user, product=product, size=size)

        if not created:
            if cart_item.quantity < product.quantity:  # Ensure stock is available
                cart_item.quantity += 1
            else:
                messages.error(req, "Not enough stock available.")
                return redirect('view_pro', pid=pid)

        cart_item.save()

        messages.success(req, 'Product added to cart successfully.')
        return redirect('view_cart')
    return redirect('eazy_login')




from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Cart, ProductSize

def update_cart_quantity(request, cart_id, action):
    # Retrieve the cart item
    cart_item = get_object_or_404(Cart, id=cart_id)
    
    size = cart_item.size  # Size of the product in the cart
    product = cart_item.product

    # Fetch the stock for this size
    product_size = ProductSize.objects.filter(product=product, size=size).first()
    
    if not product_size:
        messages.error(request, f"Size {size.size} is unavailable.")
        return redirect('view_cart')

    available_stock = product_size.quantity  # Available stock for this size
    item_price = product.offer_price if product.offer_price else product.price  # Use offer price if available

    # Handle increasing the quantity
    if action == "increase":
        if cart_item.quantity < available_stock:
            cart_item.quantity = F('quantity') + 1  # Increase quantity
        else:
            messages.warning(request, f"Only {available_stock} items available in stock.")
    
    # Handle decreasing the quantity
    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity = F('quantity') - 1  # Decrease quantity
        else:
            cart_item.delete()  # Remove item from cart
            messages.success(request, f"Removed {cart_item.product.name} from cart.")
            return redirect('view_cart')

    # Update total price based on the new quantity
    cart_item.total_price = F('quantity') * item_price

    # Save updates
    cart_item.save(update_fields=['quantity', 'total_price'])

    messages.success(request, f"Updated cart: {cart_item.product.name}, Quantity: {cart_item.quantity}")
    return redirect('view_cart')  # Redirect back to cart view page




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
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import User, Cart, Product, Size, ProductSize, Buy

def user_buy(req, pid):
    """ Handles buying a product from the cart and marks it as paid """
    user = get_object_or_404(User, username=req.session.get('user'))
    
    # Fetch the cart item
    cart = get_object_or_404(Cart, pk=pid)
    size_name = req.POST.get('size')

    if not size_name:
        messages.error(req, "Please select a size.")
        return redirect('view_cart')

    size = get_object_or_404(Size, size=size_name)
    product = cart.product
    quantity_to_buy = cart.quantity
    total_price = cart.total_price  

    with transaction.atomic():
        # Lock the specific size stock for the product
        product_size = ProductSize.objects.select_for_update().filter(product=product, size=size).first()

        # Check if the size exists and if there is sufficient stock
        if not product_size:
            messages.error(req, f'Sorry, size {size.size} is not available for this product.')
            return redirect('view_cart')

        if product_size.quantity < quantity_to_buy:
            messages.error(req, f'Sorry, only {product_size.quantity} items are available in size {size.size}.')
            return redirect('view_cart')

        # Reduce stock for the selected size atomically
        product_size.quantity = F('quantity') - quantity_to_buy
        product_size.save(update_fields=['quantity'])

        # Update the total product stock after purchase
        total_stock = ProductSize.objects.filter(product=product).aggregate(total=Sum('quantity'))['total'] or 0
        product.quantity = total_stock
        product.save(update_fields=['quantity'])

        # Fetch an existing Buy entry instead of creating a duplicate
        buy_entry = Buy.objects.filter(user=user, product=product, size=size).first()

        if buy_entry:
            # Update the existing entry
            buy_entry.quantity = F('quantity') + quantity_to_buy
            buy_entry.price = F('price') + total_price
            buy_entry.payment_status = "Paid"  # Set payment to Paid
            buy_entry.save(update_fields=['quantity', 'price', 'payment_status'])
        else:
            # Create a new entry only if one does not exist and mark as paid
            Buy.objects.create(
                user=user, product=product, size=size, quantity=quantity_to_buy, 
                price=total_price, payment_status="Paid"
            )

        # Remove the cart item after successful purchase
        cart.delete()

    return redirect('order_page')




from django.db.models import Sum

def user_buy1(req, pid):
    user = User.objects.get(username=req.session['user'])
    product = get_object_or_404(Product, pk=pid)
    
    size_name = req.POST.get('size')
    quantity = int(req.POST.get('quantity', 1))

    if not size_name:
        messages.error(req, "Please select a size.")
        return redirect('view_pro', pid=pid)

    size = get_object_or_404(Size, size=size_name)
    product_size = get_object_or_404(ProductSize, product=product, size=size)

    if product_size.quantity >= quantity:
        
        product_size.save()

        # Update total product stock
        product.quantity = ProductSize.objects.filter(product=product).aggregate(total=Sum('quantity'))['total'] or 0
        product.save()

        price = product.offer_price * quantity
        Buy.objects.create(user=user, product=product, price=price, size=size, quantity=quantity)

      
        return redirect('order_page')
    else:
        messages.error(req, 'Insufficient stock for the selected size.')
        return redirect(view_pro, pid=pid)







                                            
                                            


from django.utils import timezone

from django.utils import timezone

def user_booking(req):
    user = get_object_or_404(User, username=req.session['user'])
    buy = Buy.objects.filter(user=user, payment_status="Paid").order_by('-date')  # Only show paid orders

    enriched_buy = []
    for order in buy:
        enriched_buy.append({
            'product': order.product,
            'price': order.price,
            'size': order.size,
            'order_id': order.id,
            'status': order.status,
            'quantity': order.quantity,
            'name': user.userprofile.name if hasattr(user, 'userprofile') and user.userprofile.name else 'No address provided',
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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import Buy, Order
from .forms import OrderForm

def order_page(request):
    if request.user.is_authenticated:
        user = request.user  # Get logged-in user
        
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                # ✅ Process and Save Order
                order = form.save(commit=False)
                order.user = user  # Link order to the user
                order.save()

                # ✅ Fetch the latest Buy object for this user
                buy = Buy.objects.filter(user=user).order_by('-id').first()

                if not buy:
                    messages.error(request, "⚠️ No valid purchase record found! Please try again.")
                    return redirect('order_page')

                messages.success(request, "🎉 Order placed successfully! Redirecting to payment...")

                # ✅ Redirect to Razorpay order creation with correct `buy.id`
                return redirect(reverse('create_razorpay_order', args=[buy.id]))

            else:
                messages.error(request, "⚠️ Order form is invalid. Please check your details.")

        else:
            # ✅ Pre-fill form with user details
            form = OrderForm(initial={'user': user})
        
        return render(request, 'user/order.html', {'form': form})

    else:
        messages.warning(request, "⚠️ You must be logged in to place an order.")
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






from django.shortcuts import render, redirect
from django.contrib import messages
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

    # Check if the profile is already fully completed (first time filling profile)
    if profile.name and profile.address and not profile.is_filled:
        # If name and address are filled for the first time, mark profile as filled
        profile.is_filled = True
        profile.save()
        messages.success(request, "Profile updated successfully! Proceeding to shop.")
        return redirect('userprd')  # Redirect to the 'userprd' page after first-time profile fill

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save the form data
            form.save()

            # If the profile fields (like name or address) are filled, redirect to userprd (shop page)
            if profile.name and profile.address and not profile.is_filled:
                profile.is_filled = True  # Mark profile as filled after first-time completion
                profile.save()
                messages.success(request, "Profile updated successfully! Proceeding to shop.")
                return redirect('userprd')  # Redirect to the 'userprd' page after successful submission

            # Success message for updating the profile (without going to userprd)
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('user_profile')  # Redirect back to the profile page after saving

    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'user/profile.html', {'form': form})




from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum
from .models import Buy, Product, ProductSize  # Import necessary models

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
        return redirect('user_booking')

    # Ensure that the order can be canceled (status is not already canceled or processed)
    if buy.status == 'Canceled':
        messages.error(request, f"Order {pid} has already been canceled.")
        return redirect('user_booking')

    # Mark the order as canceled
    buy.status = 'Canceled'

    # Restock the product size (based on quantity in the order)
    product_size = get_object_or_404(ProductSize, product=buy.product, size=buy.size)  # Get the specific product size
    
    # Increase the product size stock
    product_size.quantity += buy.quantity
    product_size.save()

    # Recalculate overall product stock based on all size quantities
    total_quantity = ProductSize.objects.filter(product=buy.product).aggregate(total=Sum('quantity'))['total'] or 0
    buy.product.quantity = total_quantity  # Update the total product quantity
    buy.product.save()  # Save the updated product stock quantity

    # Save the canceled order status
    buy.save()

    # Provide feedback to the user
    messages.success(request, f"Order {pid} has been successfully canceled, and the product has been restocked.")

    return redirect('user_booking')






    



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





from django.db import transaction
from django.db.models import F, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, Product, Size, Buy, ProductSize

def buy_all(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to make a purchase.")
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    with transaction.atomic():
        for item in cart_items:
            product = item.product
            quantity = item.quantity
            size_name = item.size

            size = get_object_or_404(Size, size=size_name)
            product_size = ProductSize.objects.select_for_update().filter(product=product, size=size).first()

            if not product_size or product_size.quantity < quantity:
                messages.error(request, f"Insufficient stock for {product.name} (Size {size.size}). Purchase failed.")
                return redirect('view_cart')

            # Deduct size-specific stock atomically
            ProductSize.objects.filter(product=product, size=size).update(quantity=F('quantity') )

            # Update total product stock
            total_stock = ProductSize.objects.filter(product=product).aggregate(total=Sum('quantity'))['total'] or 0
            product.quantity = total_stock
            product.save(update_fields=['quantity'])

            price = product.offer_price * quantity if product.offer_price else product.price * quantity

            # Update existing Buy entry or create a new one
            buy_entry, created = Buy.objects.get_or_create(
                user=request.user, product=product, size=size,
                defaults={'quantity': quantity, 'price': price}
            )

            if not created:
                Buy.objects.filter(pk=buy_entry.pk).update(
                    quantity=F('quantity') + quantity,
                    price=F('price') + price
                )

        # Clear cart after successful purchase
        cart_items.delete()
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, F
import razorpay
from django.conf import settings
from django.urls import reverse
from django.db import transaction
from .models import Buy, ProductSize, Product

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_razorpay_order(request, buy_id):
    buy = get_object_or_404(Buy, id=buy_id)

    # Ensure stock is available before proceeding
    product_size = get_object_or_404(ProductSize, product=buy.product, size=buy.size)

    if product_size.quantity < buy.quantity:
        messages.error(request, "Insufficient stock available.")
        return redirect("userprd")  # Redirect user back to product page

    order_amount = int(buy.price * 100)  # Convert to paisa
    order_currency = "INR"
    order_receipt = f"order_rcpt_{buy.id}"

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create({
        "amount": order_amount,
        "currency": order_currency,
        "receipt": order_receipt,
        "payment_capture": 1
    })

    # Save Razorpay Order ID
    buy.razorpay_order_id = razorpay_order['id']
    buy.save()

    return render(request, 'user/payment.html', {
        "order_id": razorpay_order['id'],
        "amount": order_amount,
        "key": settings.RAZORPAY_KEY_ID,
        "buy": buy,
        "callback_url": request.build_absolute_uri(reverse("payment_success"))
    })


from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
import razorpay
from django.db.models import Sum, F
from django.conf import settings
from django.urls import reverse
from django.db import transaction
from .models import Buy, ProductSize, Product

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("razorpay_payment_id")
        signature = request.POST.get("razorpay_signature")

        if not razorpay_order_id or not payment_id or not signature:
            messages.error(request, "Invalid payment details received.")
            return restore_stock_and_redirect(razorpay_order_id, "order_page")

        try:
            # Verify payment signature
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            }
            razorpay_client.utility.verify_payment_signature(params_dict)

            # Retrieve the Buy object
            buy = get_object_or_404(Buy, razorpay_order_id=razorpay_order_id)
            product_size = get_object_or_404(ProductSize, product=buy.product, size=buy.size)

            # Prevent stock from going negative
            if product_size.quantity < buy.quantity:
                messages.error(request, "Payment failed. ")
                return restore_stock_and_redirect(razorpay_order_id, "order_page")

            with transaction.atomic():
                # Deduct stock after successful payment
                product_size.quantity = F('quantity') - buy.quantity
                product_size.save(update_fields=['quantity'])

                # Update total stock in Product model
                total_stock = ProductSize.objects.filter(product=buy.product).aggregate(Sum('quantity'))['quantity__sum'] or 0
                Product.objects.filter(id=buy.product.id).update(quantity=total_stock)

                # Mark Order as Paid
                buy.payment_status = "Paid"
                buy.save(update_fields=['payment_status'])

            messages.success(request, "Payment successful! Your order has been confirmed.")
            return redirect(reverse("order_success"))

        except razorpay.errors.SignatureVerificationError:
            messages.error(request, "Payment verification failed! Please try again.")
            return restore_stock_and_redirect(razorpay_order_id, "order_page")

    messages.error(request, "Invalid request method.")
    return restore_stock_and_redirect(razorpay_order_id, "order_page")


# ✅ Function to Restore Stock if Payment Fails
# ✅ Function to Restore Stock if Payment Fails
def restore_stock_and_redirect(razorpay_order_id, redirect_page):
    """ Restore stock when payment fails and delete order """
    buy = Buy.objects.filter(razorpay_order_id=razorpay_order_id).first()

    if buy:
        product_size = ProductSize.objects.filter(product=buy.product, size=buy.size).first()
        if product_size:
            with transaction.atomic():
                # ✅ Restore stock safely for the specific size
                product_size.quantity = F('quantity') + buy.quantity
                product_size.save(update_fields=['quantity'])

                # ✅ Update total product stock
                total_stock = ProductSize.objects.filter(product=buy.product).aggregate(Sum('quantity'))['quantity__sum'] or 0
                Product.objects.filter(id=buy.product.id).update(quantity=total_stock)

        # ✅ Delete the Buy object since payment failed
        buy.delete()

    return redirect(redirect_page)

