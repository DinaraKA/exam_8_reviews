from django.conf import settings
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