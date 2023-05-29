from datetime import datetime

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from itertools import product
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.template.loader import get_template

from seller.models import seller_product
from antiqueapp.models import Category,product,Address
from cart.models import OrderPlaced
from django.urls import reverse
from django.utils.text import slugify

# Create your views here.



def seller(request):
    user=request.user
    products = product.objects.filter(user_id=user.id)
    # print(products,'#################################')
    return render(request, "seller.html", {'products': products})

def addproduct(request):
    user=request.user
    categories = Category.objects.all()
    if request.method == "POST":
        category_id = request.POST.get('cate')
        category = Category.objects.get(id=category_id)
        print(category,"***********************************************")
        pname = request.POST.get('pname')
        pdesc = request.POST.get('pdesc')
        pimg = request.POST.get('pimg')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        new_product =product(
            user=user,
            name=pname,
            descripton=pdesc,
            slug=slugify(pname),
            availabe=True,
            image=pimg,
            price=price,
            category=category,
            stock=stock,
        )
        new_product.save()
        return redirect('seller')

    return render(request, "addproduct.html", {'categories': categories})

def viewproduct(request):
    user=request.user
    products = product.objects.filter(user_id=user.id)

    return render(request, "seller.html", {'products': products})


# def vieworders(request):
#     user = request.user
#     order_details = OrderPlaced.objects.filter(is_ordered=True, product__user=user).select_related('address')
#     print(order_details,'######################### ')
#     # Use select_related to retrieve the related Address object for each OrderPlaced object

#     order_details = []
#     for order in order_details:
#         order_date = order.ordered_date
#         address = order.address
#         address_name = f"{address.fname} {address.lname}"
#         address_street = address.street
#         address_state=address.state
#         address_zip = address.zip
#         order_info = {
#             'order_date': order_date,
#             'address_name': address_name,
#             'address_street': address_street,
#             'address_zip': address_zip,
#             'address_state':address_state,
#         }
#         order_details.append(order_info)

#     return render(request, "vieworders.html", {'order_details': order_details})

def vieworders(request):
    user = request.user
    order_details = OrderPlaced.objects.filter(is_ordered=True,product_id__user_id=user)
    
    # order_details =OrderPlaced.objects.all()
    addrs=Address.objects.filter(user_id=user.id)
    # address=Address.objects.filter(user_id=user.id)
   

    return render(request, "vieworders.html", {'order_details': order_details,'addrs':addrs})




def generate_report(request):
    user = request.user
    order_details = OrderPlaced.objects.filter(user=user, is_ordered=True)
    addrs = Address.objects.filter(user=user)

    # Generate report data
    order_count = order_details.count()
    product_count = order_details.values('product').distinct().count()
    order_dates = order_details.dates('ordered_date', 'day')
    orders_per_day = order_details.values('ordered_date').annotate(count=Count('id'))

    # Render report template
    template = get_template('report1.html')
    context = {
        'user': user,
        'order_count': order_count,
        'product_count': product_count,
        'order_dates': order_dates,
        'orders_per_day': orders_per_day,
    }
    report = template.render(context)

    # Generate a unique file name for the report
    file_name = f'report1_{datetime.now().strftime("%Y%m%d%H%M%S")}.html'

    # Save the report to a file
    with open(file_name, 'w') as file:
        file.write(report)

    # Provide the report as a download to the user
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    with open(file_name, 'r') as file:
        response.write(file.read())

    return response





def logout(request):
    auth.logout(request)
    return redirect('/')