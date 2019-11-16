from django.contrib import admin

from webapp.models import Product, Review


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'description')
    list_filter = ('category',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'product', 'text', 'rating')
    list_filter = ('author','product', 'rating')


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)