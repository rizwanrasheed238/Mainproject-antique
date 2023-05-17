
from cart.models import Payment, OrderPlaced

# Register your models here.

from django.contrib import admin
from .models import OrderPlaced,Payment

class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'status', 'ordered_date']
    list_filter = ['user', 'ordered_date']
    search_fields = ['user__username', 'product__name']

admin.site.register(OrderPlaced, OrderPlacedAdmin)




class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'paid','created_at')
    list_filter = ('paid',)
    search_fields = ('user__email', 'razorpay_order_id')

admin.site.register(Payment, PaymentAdmin)

