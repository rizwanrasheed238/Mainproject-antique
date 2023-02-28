from django.db import models
from antiqueapp.models import Account
from antiqueapp.models import product



# Create your models here.

# Cart Table
class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(default=1)
    price = models.FloatField(default=0)

    def get_product_price(self):
        price = [self.product.name]
        return sum(price)

class Wishlist(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(product,on_delete=models.CASCADE)

class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField(blank=True,null=True)
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    # customer = models.ForeignKey(Address_Book, on_delete=models.SET_NULL, null=True, default=1)

    def __str__(self):
        return self.user.email

class OrderPlaced(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),

    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    def total_cost(self):
        return self.quantity




