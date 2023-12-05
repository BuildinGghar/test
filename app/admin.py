from django.contrib import admin

# Register your models here.
from .models import *
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group


admin.site.register(CityRegister)
admin.site.register(category)


class ProductsImageInline(admin.TabularInline):
    model = ProductsImage
    extra = 4
    fields = ('image',)  # Include the image field

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'city', 'product_availability', 'price', 'after_discount', 'weight')
    list_filter = ('city', 'product_availability')
    search_fields = ('name', 'long_dec')
    inlines = [ProductsImageInline]

admin.site.register(Product, ProductAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'locality', 'city', 'state', 'zipcode')
    list_filter = ('state', 'city')
    search_fields = ('name', 'locality', 'city', 'state', 'zipcode')

admin.site.register(Customer, CustomerAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'products', 'quantity', 'total_cost')
    def products(self,obj):
        link=reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link, obj.product.name)

admin.site.register(Cart, CartAdmin)



from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'paid', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id')
    search_fields = ('id', 'user__username', 'razorpay_order_id', 'razorpay_payment_id')
admin.site.register(Payment, PaymentAdmin)



class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'customers', 'products', 'quantity', 'order_date', 'status', 'total_cost' ,'payments', 'payment_status')
    search_fields = ('order__user__username', 'customer__name', 'product__name', 'order_date', 'status', 'total_amount', 'payment_status')
    ordering = ('-order_date',)
    
    def products(self,obj):
        link=reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link, obj.product.name)
    def customers(self,obj):
        link=reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link, obj.customer.name)
    def payments(self,obj):
        link=reverse("admin:app_payment_change", args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>',link, obj.payment.razorpay_payment_id)
    
admin.site.register(OrderPlaced, OrderPlacedAdmin)



@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'products')
    def products(self,obj):
        link=reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link, obj.product.name)
    
    
    
admin.site.unregister(Group)


# admin.py



# from django.contrib import admin
# from .models import OrderPlacedCOD

# from django.contrib import admin
# from django.urls import reverse
# from django.utils.html import format_html
# from .models import OrderPlacedCOD  # Import your model here

# @admin.register(OrderPlacedCOD)
# class OrderPlacedCODAdmin(admin.ModelAdmin):
#     list_display = ('user', 'order', 'product_link', 'quantity', 'customer_link', 'order_date', 'status', 'total_amount')
#     list_filter = ('status', 'user', 'order', 'product', 'customer', 'order_date', 'total_amount')
#     search_fields = ('order__user__username', 'customer__name', 'product__name', 'order_date', 'status', 'total_amount')
#     ordering = ('-order_date',)

#     def product_link(self, obj):
#         link = reverse("admin:app_product_change", args=[obj.product.pk])
#         return format_html('<a href="{}">{}</a>', link, obj.product.name)
#     product_link.short_description = 'Product'

#     def customer_link(self, obj):
#         link = reverse("admin:app_customer_change", args=[obj.customer.pk])
#         return format_html('<a href="{}">{}</a>', link, obj.customer.name)
#     customer_link.short_description = 'Customer'

#     def get_search_results(self, request, queryset, search_term):
#         queryset, use_distinct = super().get_search_results(request, queryset, search_term)

#         try:
#             search_term_as_int = int(search_term)
#             queryset |= self.model.objects.filter(product=search_term_as_int) | self.model.objects.filter(customer=search_term_as_int)
#         except ValueError:
#             pass

#         return queryset, use_distinct

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import OrderPlacedCOD  # Import your model here

@admin.register(OrderPlacedCOD)
class OrderPlacedCODAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'product_link', 'quantity', 'customer', 'order_date', 'status', 'total_amount')
    list_filter = ('status', 'user', 'order', 'product', 'customer', 'order_date', 'total_amount')
    search_fields = ('order__user__username', 'customer__name', 'product__name', 'order_date', 'status', 'total_amount')
    ordering = ('-order_date',)

    def product_link(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.name)
    product_link.short_description = 'Product'

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(product=search_term_as_int)
        except ValueError:
            pass

        return queryset, use_distinct
    

# You can register other models here if needed


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'message')
    search_fields = ('name', 'email', 'phone_number')
    list_per_page = 25

admin.site.register(ContactMessage, ContactMessageAdmin)



