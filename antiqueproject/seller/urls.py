from . import views
from django.urls import path,include



urlpatterns = [
    path('addproduct',views.addproduct,name='addproduct'),
    path('viewproduct',views.viewproduct,name='viewproduct'),
    path('deleteproduct/<int:id>/',views.deleteproduct,name='deleteproduct'),


]