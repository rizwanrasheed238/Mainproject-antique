from itertools import product
from django.conf import settings
import razorpay as razorpay
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from cart.models import Cart, Wishlist, Payment, OrderPlaced
from antiqueapp.models import Category, product, Address
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
from antiqueapp.views import sendsms

import json
from decimal import Decimal


@login_required(login_url='login')
def cart(request):
    user = request.user
    cart=Cart.objects.filter(user_id=user)
    total=0
    for i in cart:
        total += i.product.price * i.product_qty
    category=Category.objects.all()
    return render(request,'cart.html',{'cart':cart,'total':total,'category':category})

# Add to Cart.
@login_required(login_url='login')
def addcart(request, id):
    user = request.user
    item = product.objects.get(id=id)
    if item.stock > 0:
        if Cart.objects.filter(user_id=user, product_id=item).exists():
            return redirect(cart)
        else:
            product_qty = 1
            price = item.price * product_qty
            new_cart = Cart(user_id=user.id, product_id=item.id, product_qty=product_qty, price=price)
            new_cart.save()
            return redirect(cart)
    return HttpResponse("invalid stock")
#Cart Quentity Plus Settings
def plusqty(request, id):
    cart = Cart.objects.filter(id=id)
    for cart in cart:
        if cart.product.stock > cart.product_qty:
            cart.product_qty += 1
            cart.price = cart.product_qty * cart.product.price
            cart.save()
            return redirect('cart')
        # messages.success(request, 'Out of Stock')
        return redirect('cart')


# Cart Quentity Plus Settings
def minusqty(request, id):
    cart = Cart.objects.filter(id=id)
    for cart in cart:
        if cart.product_qty > 1:
            cart.product_qty -= 1
            cart.price = cart.product_qty * cart.product.price
            cart.save()
            return redirect('cart')
        return redirect('cart')


# View Cart Page
@login_required(login_url='login')
def cart(request):
    user = request.user
    cart = Cart.objects.filter(user_id=user)
    prod=product.objects.all()

    total = 0
    for i in cart:
        total += i.product.price * i.product_qty
    category = Category.objects.all()
    # subcategory = Subcategory.objects.all()
    return render(request, 'cart.html', {'cart': cart, 'total': total, 'category': category,'prod':prod})


# Remove Items From Cart
def de_cart(request, id):
    Cart.objects.get(id=id).delete()
    return redirect(cart)

def view_wishlist(request):
    user = request.user
    cart = Cart.objects.filter(user_id=user.id)
    wlist=Wishlist.objects.filter(user_id=user.id)
    return render(request,"wishlist.html",{'wlist':wlist,'cart':cart})


@login_required(login_url='login')
def add_wishlist(request,id):
    item=product.objects.get(id=id)
    user = request.user
    if Wishlist.objects.filter( user_id =user.id,product_id=item.id).exists():
        return redirect('view_wishlist')
    else:
        new_wishlist=Wishlist(user_id=user.id,product_id=item.id)
        new_wishlist.save()
        
    messages.success(request, 'Sign in..!!')
    return redirect(login)


@login_required(login_url='login')
def de_wishlist(request,id):
    Wishlist.objects.get(id=id).delete()
    return redirect('view_wishlist')


def checkout(request):
    user = request.user
    cart = Cart.objects.filter(user_id=user)
    orders = OrderPlaced.objects.filter(user_id=user)
    total = Decimal('0')
    category = Category.objects.all()

    for i in cart:
        total += i.product.price * i.product_qty

    razoramount = float(total) * 100

    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))

    data = {
        "amount": float(total),
        "currency": "INR",
        "receipt": "order_rcptid_11"
    }
    payment_response = client.order.create(data=data)

    order_id = payment_response['id']
    request.session['order_id'] = order_id
    order_status = payment_response['status']
    add = Address.objects.filter(user_id=request.user)

    if order_status == 'created':
        payment = Payment(user=request.user,
                          amount=total,
                          razorpay_order_id=order_id,
                          razorpay_payment_status=order_status)
        payment.save()

    return render(request, 'checkout.html', {'orders': orders, 'check': cart, 'total': total, 'category': category, 'razoramount': razoramount, 'address': add})

def payment_done(request):
    order_id = request.session['order_id']
    payment_id = request.GET.get('payment_id')

    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    # sendsms()
    messages.success(request, 'Thank You for ordering')

    cart = Cart.objects.filter(user=request.user)
    for c in cart:
        c.product.stock -= c.product_qty
        c.product.save()
        OrderPlaced(user=request.user, product=c.product, quantity=c.product_qty, payment=payment, is_ordered=True).save()
        c.delete()

    return redirect('home')

#pdf generate
def get(request, id, *args, **kwargs, ):
        user=request.user
        place = OrderPlaced.objects.all()
        # date = place.payment.created  _at
        orders = OrderPlaced.objects.filter(user_id=user,id=id)
        total = 0
        for o in orders:
            total = total + (o.product.price * o.quantity)
        addrs=Address.objects.filter(user_id= request.user.id)
        print(total,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        
        data = {
            "total": total,
            "orders": orders,
            "shipping": addrs,
            "user":user,
        }
        pdf = render_to_pdf('report.html', data)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            # filename = "Report_for_%s.pdf" %(data['id'])
            filename = "Bill"

            content = "inline; filename= %s" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Page Not Found")

