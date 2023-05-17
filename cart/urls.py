from . import views
from django.urls import path


urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('addcart/<int:id>/', views.addcart, name='addcart'),
    path('de_cart/<int:id>/', views.de_cart, name='de_cart'),
    path('plusqty/<int:id>/',views.plusqty,name='plusqty'),
    path('minusqty/<int:id>/',views.minusqty,name='minusqty'),
    path('wishlist/', views.Wishlist, name='wishlist'),
    path('add_wishlist/<int:id>/', views.add_wishlist, name='add_wishlist'),
    path('view_wishlist', views.view_wishlist, name='view_wishlist'),
    path('de_wishlist/<int:id>/', views.de_wishlist, name='de_wishlist'),
    path('checkout/',views.checkout,name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('pdf/<int:id>/', views.get,name='pdf'),


]