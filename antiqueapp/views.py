from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


# def index(request):
#     return render(request,"index-1.html")

from django.contrib import messages, auth
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from antiqueapp.models import product
from cart.models import OrderPlaced, Wishlist, Cart
from .models import Account, Category
from django.contrib.auth import authenticate, login
from django.db.models import Q
from antiqueapp.models import Address,Review

from django.contrib import messages

from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from django.urls import reverse


from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.http import JsonResponse
from textblob import TextBlob

from django.db.models import Avg,Sum
from antiqueapp.models import product


from datetime import timedelta
from django.utils import timezone
# from celery.task import periodic_task







def home(request):
    user = request.user
    products = product.objects.all()
    category = Category.objects.all()
    wlist = Wishlist.objects.filter(user_id=user.id)
    cart = Cart.objects.filter(user_id=user.id)
    sentiment_score = request.GET.get('sentiment_score', None)
    return render(request, 'home.html', {'datas': products, 'category': category,'sentiment_score': sentiment_score,'wlist':wlist,'cart':cart})

def products(request,id):
    user=request.user
    products = product.objects.filter(category_id=id)
    category = Category.objects.all()
    wlist = Wishlist.objects.filter(user_id=user.id)
    cart = Cart.objects.filter(user_id=user.id)
    return render(request, 'product.html', {'datas': products, 'category': category,'wlist':wlist,'cart':cart})

def customer_sentiment(request):
    products = product.objects.all()
    data = {}
    for i in products:
        reviews = Review.objects.filter(product=i)
        if reviews.exists():
            sentiment_avg = reviews.aggregate(Avg('sentiment_polarity'))['sentiment_polarity__avg']
            if sentiment_avg and sentiment_avg > 0.3:
                data[i.name] = sentiment_avg or 0
    # Sort the data by sentiment polarity in descending order
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    print(sorted_data,"##################################3")
    context = {'products': sorted_data}
    return render(request, 'home.html', context)

def productdet(request,id):
    user=request.user
    # review=Review.objects.filter(product_id=id,user_id=user)
    products = product.objects.filter(id=id)
    rreview=Review.objects.filter(product_id=id)
    cart = Cart.objects.filter(user_id=user.id)
    # print(review,"#####################################################")
    # category = Category.objects.all()
    return render(request, 'productdet.html', {'datas': products,"rev":rreview,'cart':cart})

def deal_of_day(request):
    products = product.objects.filter(is_deal_of_day=True).first()
    return render(request, 'home.html', {'product': products})





def blog(request):
    return render(request,"blog.html")

def cart(request):
    return render(request,"cart.html")


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in.')
            request.session['email'] = email

            if user.is_admin:
                return redirect('/admin/')
            
            elif user.approved_staff and user.is_staff:
                return redirect('/seller/')

            else:
                return redirect('home')

        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        fname=request.POST['fname']
        lname=request.POST['lname']
        phone_number=request.POST['phone']
        password=request.POST['password']
        cpassword = request.POST['cpassword']
        user = authenticate(email=email, password=password)
        roles = request.POST['roles']
        is_user = is_staff = False
        if roles == 'is_admin':
            is_admin = True
        if roles == 'is_user':
            is_user = True
        else:
            is_staff = True

        if Account.objects.filter(email=email).exists():
            messages.error(request, 'email already exists')
            return redirect('login')
        elif password!=cpassword:
             messages.error(request, 'password not matching')
             messages.info(request,"password not matching")
             return redirect('login')


        else:
            user=Account.objects.create_user(email=email, password=password, fname=fname, lname=lname,  phone_number=phone_number,is_staff=is_staff,is_user=is_user)
            user.save()
            messages.success(request, 'you are registered')
            messages.success(request, 'Thank you for registering with us.')
            messages.success(request, 'Please verify your email for login!')

            current_site = get_current_site(request)
            message = render_to_string('account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_mail(
                'Please activate your account',
                message,
                'medievalstore123@gmail.com',
                [email],
                fail_silently=False,
            )

            return redirect('/login/?command=verification&email=' + email)
            # return redirect('login')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

def index(request):
    products = product.objects.all()
    category = Category.objects.all()
    return render(request,'index-1.html',{'datas':products,'category':category})


def search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            multiple_q = Q(Q(name__icontains=query) | Q(descripton__icontains=query))
            products = product.objects.filter(multiple_q)
            return render(request, 'search.html', {'product': products})
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
    return render(request, 'search.html', {})



def search_products(request):
    query = request.GET.get('query')
    if query:
        multiple_q = Q(Q(name__icontains=query))
        prod = product.objects.filter(multiple_q)
    else:
        prod = product.objects.none()

    product_list = []
    for p in prod:
        product = {
            'id': p.id,
            'name': p.name,
            # 'image_url': None,
            'url': request.build_absolute_uri(reverse('productdet', args=[p.id])),
        }
        if p.image:
            image_url = settings.MEDIA_URL + str(p.image)
            product['image_url'] = request.build_absolute_uri(image_url)

        product_list.append(product)
        return JsonResponse({'products': product_list})



def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email

            current_site = get_current_site(request)
            message = render_to_string('ResetPassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_mail(
                'Please activate your account',
                message,
                'athulrizwan12345@gmail.com',
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'resetPassword.html')

def seller(request):
    return render(request, 'seller.html')

@login_required(login_url='login')
def dashboard(request):
    user=request.user
    cart = Cart.objects.filter(user_id=user.id)
    orders =OrderPlaced.objects.filter(user_id=user)
    # orders = Order.objects.order_by(
    #     '-created_at').filter(user_id=request.user.id, is_ordered=True)
    # order_count = orders.count()
    userprofile=Account.objects.get(id=request.user.id)
    item = OrderPlaced.objects.filter(user_id=user)
    context = {
        # 'orders_count': order_count,
        'cart':cart,
        'userprofile':userprofile,
        'item':item,
        'orders':orders,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def editprofile(request):
    # orders = Order.objects.order_by(
    #     '-created_at').filter(user_id=request.user.id, is_ordered=True)
    # order_count = orders.count()
    userprofile=Account.objects.get(id=request.user.id)

    if request.method == 'POST':
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        phone_number = request.POST.get("phone_number")

        userprofile.fname=fname
        userprofile.lname=lname
        userprofile.phone_number=phone_number
        userprofile.save()
        return redirect('dashboard.html')

    context = {
        # 'orders_count': order_count,
        'userprofile':userprofile,
    }
    return render(request, 'dashboard.html', context)



def address(request):
    user = request.user.id
    adrs = Address.objects.filter(user_id=user)
    print(adrs)
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        phone = request.POST.get('phone_number')

        # user = request.user.id
        # val = Seller_product.objects.all()
        # user=request.user.id
        val = Address(
             user_id=user,fname=fname, lname=lname, street=street, city=city, state=state, zip=zip,phone=phone
        )
        val.save()
        # print(cate,pname,pdesc,pimg,price,stock)
        return redirect('address')

    return render(request, "dashboard.html",{'adrs':adrs})


from .forms import AddressForm

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False) # create a new address object but don't save it yet
            address.user = request.user # set the user of the address to the current user
            address.save() # save the address object
            return redirect('address_list') # redirect to a success page or to the list of addresses
    else:
        form = AddressForm()

    return render(request, 'dashboard.html', {'form': form})


#for data visualisatiom im admin panel
import matplotlib.pyplot as plt
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from cart.models import OrderPlaced
from django.views.decorators.csrf import csrf_exempt
import matplotlib
matplotlib.use('Agg')


@csrf_exempt
def view(request):
    data = OrderPlaced.objects.filter(is_ordered=True).annotate(month=ExtractMonth('ordered_date')).values(
        'month').order_by('month')

    months = [month[1] for month in OrderPlaced.MONTH_CHOICES]

    totals = [data.filter(month=month[0]).aggregate(total=Count('id'))['total'] for month in OrderPlaced.MONTH_CHOICES]

    plt.bar(months, totals)
    plt.title('Products sold by month')
    plt.xlabel('Month')
    plt.ylabel('Total')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Convert the plot to a Django view response
    from io import BytesIO
    import base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Render the template with the plot and URLs
    context = {
        'graphic': graphic,
    }
    return render(request, 'admin/products_sold_by_month.html', context)


# @csrf_exempt
# def viewview(request):
#     from io import BytesIO
#     import base64
#     import numpy as np
#     top_products = product.objects.annotate(total_sales=Sum('orderplaced__quantity')).order_by('-total_sales')[:10]

#     labels = [product.name for product in products if not np.isnan(product.total_sales)]
#     sales = [value for value in sales if not np.isnan(value)]


#     plt.pie(sales, labels=labels, autopct='%1.1f%%')
#     plt.title('Top 10 Products by Sales')

#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     image_png = buffer.getvalue()
#     buffer.close()
#     graphic = base64.b64encode(image_png)
#     graphic = graphic.decode('utf-8')

#     # Render the template with the plot and URLs
#     context = {
#         'graphic': graphic,
#     }
#     return render(request, 'admin/top_products.html', context)    


def rateproduct(request,id):
    user=request.user
    order = get_object_or_404(OrderPlaced,id=id)
    pproduct = order.product
    rreview=Review.objects.filter(product_id=id)
    item = OrderPlaced.objects.filter(id=id)
    print(item,'33333333333333333333333333333333')
    if request.method == 'POST':
        review = request.POST['review']
        review_data = Review.objects.create(
            user=request.user,
            product=pproduct,
            review=review,
        )
        return redirect(reverse_lazy('home'))
    else:
        context = {'order': order, 'product': pproduct,'rev':rreview,'datas':item, 'productname': product.name}
        return render(request, 'productdet.html', context)






from twilio.rest import Client 
 

def sendsms(): 
    account_sid = 'AC8cc6b7182a8c135645ac147cc64950cf' 
    auth_token = '7525383d7f21fc89baa666916df0bd07' 
    client = Client(account_sid, auth_token) 
    
    message = client.messages.create(  
                                messaging_service_sid='MG3b54cd6c00080cecb79e4dc404e84fc6', 
                                body='Thank you for ordering with us.Your order has been successfull',      
                                to='+918330864643' 
                            ) 
    
    print('message sent succesfully')