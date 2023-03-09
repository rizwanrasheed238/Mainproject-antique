from django.shortcuts import render
from django.conf import settings
from itertools import product
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from seller.models import seller_product
from antiqueapp.models import Category

# Create your views here.
def addproduct(request):
    category = Category.objects.all()
    user = request.user
    if request.method == "POST":
        cate = request.POST.get('cate')
        pname = request.POST.get('pname')
        pdesc = request.POST.get('pdesc')
        pimg = request.POST.get('pimg')
        price = request.POST.get('price')
        # color = request.POST.get('color')
        # size = request.POST.get('size')
        stock = request.POST.get('stock')
        # is_active = request.POST.get('isactive')
        # in_stock = request.POST.get('instock')
        # user = request.user.id
        # val = Seller_product.objects.all()
        # user=request.user.id
        val = seller_product(
             user_id=user,category=cate, name=pname, descripton=pdesc, image=pimg, price=price, stock=stock
        )
        val.save()
        # add = seller_product.objects.filter()
        # print(cate,pname,pdesc,pimg,price,stock)
        return redirect('seller')

    return render(request, "addproduct.html",{'category':category})

def viewproduct(request):
    user = request.user
    products = seller_product.objects.filter(user_id=user)

    return render(request, "seller.html", {'products': products})

def deleteproduct(request):
    user=request.user
    item  = seller_product.objects.get(user_id=user)
    item.delete()
    return redirect(request,"seller.html")



