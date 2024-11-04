from django.shortcuts import render, redirect
from .models import Product, Order, Customer, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart
# Create your views here.
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})

def category(request, foo):
    #replace hyphens with spaces
    foo = foo.replace('-', ' ')
    #grab the category from the url
    try:
        #Look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'category': category, 'products': products})
    except:
        messages.success(request, ("That Category does not exist"))
        return redirect('home')

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            #Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            #Get their saved cart from database
            saved_cart = current_user.old_cart
            #Convert db string to a dictionary
            if saved_cart:
                #convert to dictionary using json
                converted_cart = json.loads(saved_cart)
                #Add the loaded cart dictionary to the session
                #Get the cart
                cart = Cart(request)
                #Loop through the cart and add items from the database
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, ("You are now Logged in..."))
            return redirect('home')
        else:
            messages.warning(request, ("Error Logging In - Please try again !!!"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You are now logged out !!!")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Registered Successfully !!!")
            messages.success(request, "Please Update Your Profile Informations for Billing Purposes.")
            return redirect('update_info')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request, current_user)
            messages.success(request, "Your profile has been updated successfully !!!")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.success(request, "You must be logged in to view that page !!!")
        return redirect('home')
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated successfully !!! Please Log in again.")
                # login(request, current_user)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')

        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to view that page !!!")
        return redirect('home')
   
def update_info(request):
    if request.user.is_authenticated:
        #Get Current User
        current_user = Profile.objects.get(user__id=request.user.id)
        #Get Current Users Shipping Info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        #Get Original User Form
        form = UserInfoForm(request.POST or None, instance=current_user)
        #Get User's Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        
        if form.is_valid() or shipping_form.is_valid():
            #Save original Form
            form.save()
            #Save Shipping Form
            shipping_form.save()
            
            messages.success(request, "Your Profile Info has been Updated Successfully !!!")
            return redirect('home')
        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.success(request, "You must be logged in to view that page !!!")
        return redirect('home')
    
def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        products = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched) | Q(category__name__icontains=searched)) 
        # for case insensitive searching we use __icontains. 
        # and in searching by name we use 'name__icontains'.
        if not products:
            messages.warning(request, "You didn't enter any search criteria !!!")
            return render(request, 'search.html', {'searched': searched, 'products': products})
        return render(request, 'search.html', {'searched': searched, 'products': products})
        
# superuser
# username : sabbir
# pass : sab1995
# username : admin
# pass : 123456