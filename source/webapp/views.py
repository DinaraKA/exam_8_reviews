from django.views.generic import ListView
from webapp.models import Product


class IndexView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'index.html'
