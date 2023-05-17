import base64
from io import BytesIO
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Avg,Sum
from django.http import HttpResponse
from django.urls import path
from matplotlib.patches import Patch
# from antiqueapp.views import products

from cart.models import Payment, OrderPlaced
# Register your models here.
from .models import Category, product, Account,Review


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields ={'slug':('name',)}
admin.site.register(Category,CategoryAdmin)


import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO

class MyModelAdmin(admin.ModelAdmin):
    ...

    def sales_chart(self, request):
        products = product.objects.all()
        data = {}
        Sum=0
        for i in products:
            sales = OrderPlaced.objects.filter(product=i)
            if sales.exists():
                total_sales = sales.aggregate(Sum('quantity'))['quantity__sum']
                data[i.name] = total_sales or 0

        # generate graph using matplotlib
        fig, ax = plt.subplots()
        fig.set_size_inches(20, 15)

        ax.bar(data.keys(), data.values(), color='green')
        ax.set_xlabel('Products')
        ax.set_ylabel('Total Sales')
        ax.set_title('Sales Chart')
        plt.xticks(rotation=45)

        # save graph as image and encode as base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # return HTTP response with graph as image
        response = HttpResponse(content_type='image/png')
        response.write(base64.b64decode(image))
        return response

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
           
            path('sales-chart/', self.admin_site.admin_view(self.sales_chart), name='sales-chart'),
        ]
        return custom_urls + urls

class productAdmin(admin.ModelAdmin):
    list_display = ('user','name','price','createf','stock','updated')
    list_editable = ('price',)
    prepopulated_fields ={'slug':('name',)}
    list_per_page = 20



    def top_products(self,request):
        products = product.objects.annotate(total_sales=Sum('orderplaced__quantity')).order_by('-total_sales')[:10]

        sales = [product.total_sales for product in products if isinstance(product.total_sales, (int, float))]
        labels = [product.name for product in products if isinstance(product.total_sales, (int, float))]

        plt.pie(sales, labels=labels, autopct='%1.1f%%')
        plt.title('Top 10 Products by Sales')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')

        context = {
            'graphic': graphic,
        }
        response = HttpResponse(content_type='image/png')
        response.write(base64.b64decode(graphic))
        return response

    def sentiment_graph(self, request):
        products = product.objects.all()
        data = {}
        for i in products:
            reviews = Review.objects.filter(product=i)
            if reviews.exists():
                sentiment_avg = reviews.aggregate(Avg('sentiment_polarity'))['sentiment_polarity__avg']
                data[i.name] = sentiment_avg or 0
        # generate graph using matplotlib
        fig, ax = plt.subplots()
        fig.set_size_inches(20, 15)
        colors = ['blue' if v > 0 else 'red' if v < 0 else 'green' for v in data.values()]
        ax.bar(data.keys(), data.values(), color=colors)
        ax.set_xlabel('Products')
        ax.set_ylabel('Average Sentiment Polarity')
        ax.set_title('Sentiment Analysis of Products')
        plt.xticks(rotation=45)
        handles = [Patch(facecolor='blue', label='Positive'),
                   Patch(facecolor='red', label='Negative'),
                   ]
        # plt.legend(handles=handles)
        plt.legend(handles=handles, fontsize=20)
        # save graph as image and encode as base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        # return HTTP response with graph as image
        response = HttpResponse(content_type='image/png')
        response.write(base64.b64decode(image))
        return response

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sentiment-graph/', self.admin_site.admin_view(self.sentiment_graph), name='sentiment-graph'),
            path('top-products/', self.admin_site.admin_view(self.top_products), name='top-products'),

        ]
        return custom_urls + urls

admin.site.register(product,productAdmin)

class AccountAdmin(UserAdmin):
    exclude =('password','Groups')

    list_display = (
        'email', 'fname', 'lname', 'last_login', 'is_active', 'date_joined'
    )
    list_editable = ['is_active']

    list_display_links = (
        'email', 'fname', 'lname',
    )
    readonly_fields = (
        'last_login', 'date_joined',
    )
    ordering = (
        '-date_joined',
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        return False

        # This will help you to disable delete functionaliyt

    def has_delete_permission(self, request, obj=None):
        return False



admin.site.register(Account, AccountAdmin)


# admin.site.register(ReviewRating)



