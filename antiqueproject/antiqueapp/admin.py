import base64
from io import BytesIO

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Avg
from django.http import HttpResponse
from django.urls import path
from matplotlib import pyplot as plt

from cart.models import Payment, OrderPlaced
# Register your models here.
from .models import Category, product, Account,ReviewRating,Review


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields ={'slug':('name',)}
admin.site.register(Category,CategoryAdmin)

class productAdmin(admin.ModelAdmin):
    list_display = ('name','price','availabe','createf','updated')
    list_editable = ('price',)
    prepopulated_fields ={'slug':('name',)}
    list_per_page = 20

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
        ax.bar(data.keys(), data.values())
        ax.set_xlabel('Products')
        ax.set_ylabel('Average Sentiment Polarity')
        ax.set_title('Best Product based on Sentiment Analysis')
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
            path('sentiment-graph/', self.admin_site.admin_view(self.sentiment_graph), name='sentiment-graph'),
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


admin.site.register(ReviewRating)