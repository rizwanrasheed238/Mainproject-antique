from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from cart.models import Payment, OrderPlaced
# Register your models here.
from .models import Category, product, Account


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields ={'slug':('name',)}
admin.site.register(Category,CategoryAdmin)

class productAdmin(admin.ModelAdmin):
    list_display = ('name','price','availabe','createf','updated')
    list_editable = ('price',)
    prepopulated_fields ={'slug':('name',)}
    list_per_page = 20
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

