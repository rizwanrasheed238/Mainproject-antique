from django.contrib import admin

from cart.models import Payment, OrderPlaced

# Register your models here.
admin.site.register(OrderPlaced)
admin.site.register(Payment)