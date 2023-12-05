# sitemaps.py

from django.contrib.sitemaps import Sitemap
from .models import CityRegister, category, Product, ProductsImage, Customer, Cart, Wishlist, Payment, OrderPlaced, OrderPlacedCOD, ContactMessage

class CityRegisterSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return CityRegister.objects.all()

class CategorySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return category.objects.all()

class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return Product.objects.all()

class ProductsImageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return ProductsImage.objects.all()

class CustomerSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Customer.objects.all()

class CartSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Cart.objects.all()

class WishlistSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Wishlist.objects.all()

class PaymentSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return Payment.objects.all()

class OrderPlacedSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return OrderPlaced.objects.all()

class OrderPlacedCODSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return OrderPlacedCOD.objects.all()

class ContactMessageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return ContactMessage.objects.all()
