from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ProductReviewForm
from webapp.models import Product, Review


class IndexView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'index.html'


class ProductView(DetailView):
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['product'].product_review.order_by('rating')
        self.paginate_reviews_to_context(products, context)
        return context

    def paginate_reviews_to_context(self, reviews, context):
        paginator = Paginator(reviews, 3, 0)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        context['paginator'] = paginator
        context['page_obj'] = page
        context['reviews'] = page.object_list
        context['is_paginated'] = page.has_other_pages()


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'product/product_create.html'
    fields = ['image', 'name', 'category', 'description']

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'product/product_update.html'
    fields = ['image', 'name', 'category', 'description']
    context_object_name = 'product'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/product_delete.html'
    success_url = reverse_lazy('webapp:index')


class ProductReviewCreateView(CreateView):
    template_name = 'review/review_add.html'
    form_class = ProductReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(pk=self.kwargs['pk'])
        context['product'] = product
        return context

    def form_valid(self, form):
        product_pk = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_pk)
        product.product_review.create(author = self.request.user, **form.cleaned_data)
        return redirect('webapp:product_detail', pk=product_pk)


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    template_name = 'review/review_update.html'
    fields = ['text', 'rating']
    context_object_name = 'review'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


