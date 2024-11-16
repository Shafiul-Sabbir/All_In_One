from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product, Profile
import datetime
# Import Some Paypal Stuff
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid # For generating unique user id for duplicate orders
# Create your views here.

def order_details(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #Get the order
        order = Order.objects.get(pk=pk)
        # print(order)
        #Get the order items
        order_items = OrderItem.objects.filter(order=order)
        
        #Get the order subtotal
        items_subtotal_list = []
        for item in order_items:
            item_subtotal = item.quantity * (item.product.sale_price if item.product.is_sale else item.product.price)
            items_subtotal_list.append(item_subtotal)
        order_subtotal = sum(items_subtotal_list)
        
         # Zip order items with their subtotals
        order_items_with_subtotals = zip(order_items, items_subtotal_list)
        
        #Get the shipping address
        address = Order.objects.get(pk=order.id).shipping_address
        
        if request.POST:
            status =  request.POST['shipping_status']
            #check if true or false
            if status == "true":
                order = Order.objects.filter(id=pk)
                # update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order = Order.objects.filter(id=pk)
                # update the status
                order.update(shipped=False)
            messages.success(request, "Shipping Status Updated Successfully !!!")
            return redirect('order_details', pk=pk)
        
        context = {'order': order, 
                   'order_items': order_items, 'order_subtotal' : order_subtotal, 'order_items_with_subtotals': order_items_with_subtotals,
                   'address': address}
        
        return render(request, 'payment/order_details.html', context)

    else:
        messages.success("Access Denied")
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False).order_by('-date_ordered')
        
        if request.POST:
            status =  request.POST['shipping_status']
            num =  request.POST['num']

            #Grab Date and Time
            now = datetime.datetime.now()
            #Grab the order
            order = Order.objects.filter(id=num)
            # update the status
            order.update(shipped=True, date_shipped=now)
            messages.success(request, "Shipping Status Updated Successfully !!!")
            return redirect('not_shipped_dash')

        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})
    else:
        messages.success("Access Denied")
        return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True).order_by('-date_ordered')
        if request.POST:
            status =  request.POST['shipping_status']
            num =  request.POST['num']

            #Grab Date and Time
            now = datetime.datetime.now()
            #Grab the order
            order = Order.objects.filter(id=num)
            # update the status
            order.update(shipped=False)
            messages.success(request, "Shipping Status Updated Successfully !!!")
            return redirect('shipped_dash')
        
        return render(request, 'payment/shipped_dash.html', {'orders': orders})
    else:
        messages.success("Access Denied")
        return redirect('home')


def process_order(request):
    if request.POST:
        #Get the Cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        
        #Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        #Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')
        #Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        
        #create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
        
        # print(shipping_address)
        amount_paid = totals
        
        #create an Order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            
            create_order.save()
            
            #Create Order Items
            #Get the order id
            order_id = create_order.pk
            
            #Get product Info
            for product in cart_products:
                #Get product id
                product_id = product.pk
                #Get product price
                if product.is_sale:
                    price = product.sale_price
                else:       
                    price = product.price
                    
                #Get product quantity
                for key, value in quantities.items():
                    if int(key) == product.pk:
                        product_quantity = value  
                        #Create OrderItem
                        create_order_item = OrderItem(order=create_order, product=product, user=user, quantity=product_quantity,price=price, )
                        
                        create_order_item.save()
                
            #Delete Our Cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]
                    
            #Delete the cart from Database (Old cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            #Delete shopping cart in database
            current_user.update(old_cart="")
            
            messages.success(request, "Your order has been placed successfully !!!")
            return render(request, 'payment/process_order.html', {})
        
        else:
            # not logged in 
            #create Order
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            
            create_order.save()
            
            #Create Order Items
            #Get the order id
            order_id = create_order.pk
            
            #Get product Info
            for product in cart_products:
                #Get product id
                product_id = product.pk
                #Get product price
                if product.is_sale:
                    price = product.sale_price
                else:       
                    price = product.price
                    
                #Get product quantity
                for key, value in quantities.items():
                    if int(key) == product.pk:
                        product_quantity = value  
                        #Create OrderItem
                        create_order_item = OrderItem(order=create_order, product=product, quantity=product_quantity,price=price, )
                        
                        create_order_item.save()
                
            #Delete Our Cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
        
            messages.success(request, "Your order has been placed successfully !!!")
            return render(request, 'payment/process_order.html', {})
    
    else:
        messages.success(request, "Access Denied !!!")
        return redirect ('home')

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})

def  payment_failed(request):
    return render(request, 'payment/payment_failed.html', {})

def payment_ipn(rquest):
    return render(rquest, 'payment/payment_ipn.html', {})

def checkout(request):
    #Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
        # CheckOut as logged in user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
    else:
        # checkOut as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
   
def billing_info(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        
        #Create a session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        
        # Get the Host 
        host = request.get_host()
        # Create Paypal Form Dictionary
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': totals,
            'item_name': 'Book Order',
            'no_shipping' : '2',
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host, reverse('payment-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('payment_success')),
            'cancel_return': 'http://{}{}'.format(host, reverse('payment_failed')),
        }
        
        #Create the Paypal Form
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

        
        # check to see if user is logged in 
        if request.user.is_authenticated:
            # Get the Billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, "billing_form": billing_form, "paypal_form": paypal_form}) 

        else:
            # not logged in 
            # Get the Billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, "billing_form": billing_form, "paypal_form": paypal_form})
    
    else:
        messages.success(request, "You must be logged in to view that page !!!")
        return redirect ('home')
