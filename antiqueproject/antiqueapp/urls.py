from django.contrib import admin

from . import views
from django.urls import path,include

from .admin import productAdmin

urlpatterns = [
    path('index/',views.index,name='index'),
    path('', views.home, name="home"),
    # path('score/<int:sentiment_score>/', views.home, name='home'),

    path('login/',views.login,name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('products/', views.products, name="products"),
    path('productdet/<int:id>/', views.productdet, name="productdet"),
    path('Category/', views.Category, name="category"),
    # path('cart/', views.cart, name="cart"),
    path('blog/', views.blog, name="blog"),
    path('search/',views.search,name="search"),
    path('seller/',views.seller,name="seller"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('address/',views.address,name='address'),
    path('view/', views.view, name='view'),
    path('recommendations/', views.recommend_products, name='recommendations'),
    path('review/<int:id>/', views.rateproduct, name='review'),
    path('admin/antiqueapp/product/sentiment-graph/', admin.site.admin_view(productAdmin.sentiment_graph), name='sentiment-graph'),

]
