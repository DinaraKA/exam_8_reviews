from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


CATEGORY_CHOICES = (
    ('other', 'Other'),
    ('book', 'Book'),
    ('hotel', 'Hotel'),
    ('car', 'Car')
)

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Product')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES[0][0],
                                verbose_name='Category')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Description')
    image = models.ImageField(upload_to='product_images', null=True, blank=True, verbose_name='Image')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


RATING_CHOICES = (
    (5, 'excellent'),
    (4, 'good'),
    (3, 'so-so'),
    (2, 'bad'),
    (1, 'awful')
)


class Review(models.Model):
    author = models.ForeignKey(User, related_name='user_review', on_delete=models.PROTECT, verbose_name='Author')
    product = models.ForeignKey(Product, related_name='product_review', on_delete=models.PROTECT,
                                    verbose_name='Product')
    text = models.TextField(max_length=1000, verbose_name='Text')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Rating')


    def __str__(self):
        return str(self.author.username)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'