from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


# def index(request):
#     return render(request,"index-1.html")

from django.contrib import messages, auth
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy

from cart.models import OrderPlaced, Wishlist, Cart
from .models import Account, Category, product, ReviewRating
from django.contrib.auth import authenticate
from django.db.models import Q
from antiqueapp.models import Address,Review
from .forms import ReviewForm
from django.contrib import messages


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

from django.db.models import Avg
from antiqueapp.models import product, Rating
from surprise import SVD
from surprise import Dataset
from surprise import Reader


def products(request):
    products = product.objects.all()
    category = Category.objects.all()
    return render(request, 'product.html', {'datas': products, 'category': category})

def home(request):
    user = request.user
    products = product.objects.all()
    category = Category.objects.all()
    wlist = Wishlist.objects.filter(user_id=user.id)
    cart = Cart.objects.filter(user_id=user.id)

    sentiment_score = request.GET.get('sentiment_score', None)
    return render(request, 'home.html', {'datas': products, 'category': category,'sentiment_score': sentiment_score,'wlist':wlist,'cart':cart})


def productdet(request,id):
    products = product.objects.filter(id=id)
    # category = Category.objects.all()
    return render(request, 'productdet.html', {'datas': products})





@login_required
def recommend_products(request):
    # Get all the products in the database
    products = product.objects.all()

    # Create a dictionary of the ratings for each product
    product_ratings = {}
    for product in products:
        ratings = Rating.objects.filter(product=product)
        if ratings:
            product_ratings[product.id] = round(ratings.aggregate(Avg('value'))['value__avg'], 2)

    # Load the data into the Surprise library
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_dict(product_ratings, reader)
    trainset = data.build_full_trainset()

    # Train the SVD algorithm on the data
    algo = SVD()
    algo.fit(trainset)

    # Get the top 5 recommended products for the current user
    current_user = request.user
    user_ratings = Rating.objects.filter(user=current_user)
    user_product_ids = [rating.product.id for rating in user_ratings]
    testset = trainset.build_anti_testset()
    testset = filter(lambda x: x[0] == current_user.id, testset)
    predictions = algo.test(testset)
    top_n = sorted(predictions, key=lambda x: x.est, reverse=True)[:5]
    recommended_products = [product.objects.get(id=pred.iid) for pred in top_n]
    print(recommended_products,"******************************************************8")
    return render(request, 'productdet.html', {'products': recommended_products})


def blog(request):
    return render(request,"blog.html")

def cart(request):
    return render(request,"cart.html")

def login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        user=authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are logged in')
            request.session['email']=email

            if user.is_admin:
                return redirect('/admin/')
            elif user.approved_staff:
                return redirect('seller')

            elif user.is_user:
                return redirect('home')
            else:
                messages.success(request, 'invalid email')
                return redirect('register')



        else:
            messages.success(request, 'invalid login credentials')
            return redirect('register')
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

        print(email,password,fname,lname,phone_number)
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
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            multiple_q = Q(Q(name__icontains=query) | Q(descripton__icontains=query))
            products = product.objects.filter(multiple_q)
            return render(request, 'search.html', {'product':products})
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
    return render(request, 'search.html', {})



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
                'medievalstore123@gmail.com',
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
    # orders = Order.objects.order_by(
    #     '-created_at').filter(user_id=request.user.id, is_ordered=True)
    # order_count = orders.count()
    userprofile=Account.objects.get(id=request.user.id)
    item = OrderPlaced.objects.filter(user_id=user)
    context = {
        # 'orders_count': order_count,
        'userprofile':userprofile,
        'item':item,
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





def rateproduct(request,id):
    order = get_object_or_404(OrderPlaced,id=id)
    product = order.product
    if request.method == 'POST':
        review = request.POST['review']
        review_data = Review.objects.create(
            user=request.user,
            product=product,
            review=review,
        )
        return redirect(reverse_lazy('home'))
    else:
        context = {'order': order, 'product': product, 'productname': product.name}
        return render(request, 'review.html', context)

