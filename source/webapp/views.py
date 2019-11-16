from django.views.generic import ListView, DetailView

from webapp.models import Product


class IndexView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'index.html'

class ProductView(DetailView):
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'