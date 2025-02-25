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
from django.shortcuts import redirect

def eazy_logout(req):
    req.session.flush()          # Delete session
    logout(req)
    
    # Add confirmation message
    messages.success(req, 'You have been logged out successfully.')
    
    # Redirect to login page
    return redirect('eazy_login')





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


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Buy, Order

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
                        messages.success(req, f"Order {buy_id} status updated to {value}.")
                    else:
                        messages.info(req, f"Order {buy_id} status is already {value}.")
                except Buy.DoesNotExist:
                    messages.error(req, f"Order {buy_id} not found.")
        return redirect('booking')

    # Fetch Buy objects and their associated Orders
    buys = Buy.objects.all().order_by('-date')
    combined_data = []

    for buy in buys:
        order = Order.objects.filter(buy=buy).first()  # Get the correct order linked to this Buy
        
        # Ensure there's always an order linked to Buy
        if not order:
            order = Order.objects.create(
                buy=buy,
                customer_name=buy.user.username,
                phone_number=buy.user.userprofile.phone_number if hasattr(buy.user, 'userprofile') else "N/A",
                email=buy.user.email if buy.user.email else "N/A",
                address=buy.user.userprofile.address if hasattr(buy.user, 'userprofile') else "N/A",
            )

        combined_data.append({'buy': buy, 'order': order})

    return render(req, 'shop/booking.html', {'combined_data': combined_data})


def create_order(request, buy_id):
    buy = Buy.objects.get(id=buy_id)

    # First, check if an Order already exists
    order = Order.objects.filter(buy=buy).first()

    if order:
        messages.info(request, f"An order already exists for {buy.product.name}. No duplicate created.")
    else:
        # Create new Order only if none exists
        order = Order.objects.create(
            buy=buy,
            customer_name=buy.user.username,
            phone_number=buy.user.userprofile.phone_number if hasattr(buy.user, 'userprofile') else "",
            email=buy.user.email,
            address=buy.user.userprofile.address if hasattr(buy.user, 'userprofile') else "",
        )
        messages.success(request, f"Order for {buy.product.name} created successfully!")

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
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import User, Cart, Product, Size, ProductSize, Buy

def user_buy(req, pid):
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

        if not product_size or product_size.quantity < quantity_to_buy:
            messages.error(req, f'Sorry, size {size.size} is out of stock.')
            return redirect('view_cart')

        # Reduce stock for the selected size atomically
        

        # Update total product stock after purchase
        total_stock = ProductSize.objects.filter(product=product).aggregate(total=Sum('quantity'))['total'] or 0
        product.quantity = total_stock
        product.save(update_fields=['quantity'])

        # Update existing Buy entry or create a new one
        buy_entry, created = Buy.objects.get_or_create(
            user=user, product=product, size=size,
            defaults={'quantity': quantity_to_buy, 'price': total_price}
        )

        if not created:
            Buy.objects.filter(pk=buy_entry.pk).update(
                quantity=F('quantity') + quantity_to_buy,
                price=F('price') + total_price
            )

        # Remove the cart item after successful purchase
        cart.delete()

    messages.success(req, f'Product "{product.name}" (Size {size.size}) purchased successfully!')
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
        product_size.quantity = quantity
        product_size.save()

        # Update total product stock
        product.quantity = ProductSize.objects.filter(product=product).aggregate(total=Sum('quantity'))['total'] or 0
        product.save()

        price = product.offer_price * quantity
        Buy.objects.create(user=user, product=product, price=price, size=size, quantity=quantity)

        messages.success(req, f'{quantity} Product(s) purchased successfully!')
        return redirect('order_page')
    else:
        messages.error(req, 'Insufficient stock for the selected size.')
        return redirect(view_pro, pid=pid)







                                            
                                            


from django.utils import timezone

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
            'quantity': order.quantity,  # Add the quantity to the context
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
                # Process the order and save it
                order = form.save(commit=False)
                order.user = user  # Link order to the user
                order.save()

                # ✅ Fetch the latest Buy object for this user
                buy = Buy.objects.filter(user=user).order_by('-id').first()

                if not buy:
                    messages.error(request, "No valid Buy record found!")
                    return redirect('order_page')

                messages.success(request, "Order placed successfully.")
                
                # ✅ Redirect to Razorpay order creation with correct `buy.id`
                return redirect(reverse('create_razorpay_order', args=[buy.id]))

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

    messages.success(request, "Your order has been placed successfully.")
    return redirect('order_page')  # Update with your actual order page URL


import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Buy, ProductSize

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_razorpay_order(request, buy_id):
    buy = get_object_or_404(Buy, id=buy_id)
    
    # Check and update stock for the purchased product size
    try:
        product_size = ProductSize.objects.get(product=buy.product, size=buy.size)
    except ProductSize.DoesNotExist:
        return render(request, 'user/insufficient_stock.html', {
            "message": "Product size information not available."
        })
    
    if product_size.quantity >= buy.quantity:
        product_size.quantity -= buy.quantity
        product_size.save()
        
        # Recalculate overall product stock based on all size quantities
        total_quantity = ProductSize.objects.filter(product=buy.product).aggregate(total=Sum('quantity'))['total'] or 0
        buy.product.quantity = total_quantity
        buy.product.save()
    else:
        return render(request, 'user/insufficient_stock.html', {
            "message": "Insufficient stock available for this product."
        })
    
    order_amount = int(buy.price * 100)  # Convert INR to paisa
    order_currency = "INR"
    order_receipt = f"order_rcpt_{buy.id}"

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create({
        "amount": order_amount,
        "currency": order_currency,
        "receipt": order_receipt,
        "payment_capture": 1
    })

    # If in Live Mode, generate a UPI Payment Link (for a QR Code)
    if getattr(settings, "RAZORPAY_MODE", "TEST") == "LIVE":
        payment_link = razorpay_client.payment_link.create({
            "amount": order_amount,
            "currency": "INR",
            "accept_partial": False,
            "expire_by": 1735689600,  # Adjust expiry timestamp as needed
            "reference_id": f"order_{buy.id}",
            "description": f"UPI Payment for {buy.product.name}",
            "customer": {
                "name": request.user.username,
                "email": request.user.email
            },
            "notify": {"sms": True, "email": True},
            "reminder_enable": True,
            "upi_link": True  # Enables UPI Payment Link (QR Code)
        })
        qr_code_url = payment_link.get("short_url", "")
    else:
        # In test mode, UPI Payment Links are not supported.
        qr_code_url = ""
    
    buy.razorpay_order_id = razorpay_order['id']
    buy.save()

    return render(request, 'user/payment.html', {
        "order_id": razorpay_order['id'],
        "amount": order_amount,
        "key": settings.RAZORPAY_KEY_ID,
        "qr_code_url": qr_code_url,
        "buy": buy,
    })



def payment_success(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("razorpay_payment_id")
        signature = request.POST.get("razorpay_signature")

        try:
            # Verify payment signature
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)

            # Update order status
            buy = get_object_or_404(Buy, razorpay_order_id=razorpay_order_id)
            buy.payment_status = "Paid"
            buy.save()

            messages.success(request, "Payment successful!")
            return redirect(order_success)

        except razorpay.errors.SignatureVerificationError:
            messages.error(request, "Payment verification failed!")
            return redirect(order_page)

   
