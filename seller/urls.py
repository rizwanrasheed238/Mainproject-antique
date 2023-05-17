from . import views
from django.urls import path,include



urlpatterns = [
    path('addproduct',views.addproduct,name='addproduct'),
    path('seller', views.seller, name='seller'),
    path('viewproduct',views.viewproduct,name='viewproduct'),
    path('vieworders',views.vieworders,name='vieworders'),

    # path('deleteproduct/<int:id>/',views.deleteproduct,name='deleteproduct'),
    path('logout/', views.logout, name="logout"),


]