from django.shortcuts import render
from django.conf import settings
from itertools import product
from django.shortcuts import render, redirect
from django.contrib import messages, auth
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




# def deleteproduct(request, id):

#         item = seller_product.objects.get(id=id)
#         item.delete()
#         return redirect(reverse('seller'))


def logout(request):
    auth.logout(request)
    return redirect('/')