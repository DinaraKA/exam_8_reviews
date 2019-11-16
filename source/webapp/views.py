from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
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


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'product/product_create.html'
    fields = ['image', 'name', 'category', 'description']
    permission_required = 'webapp.add_product'
    permission_denied_message = 'Access is denied!'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'product/product_update.html'
    fields = ['image', 'name', 'category', 'description']
    context_object_name = 'product'
    permission_required = 'webapp.change_product'
    permission_denied_message = 'Access is denied!'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/product_delete.html'
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_product'
    permission_denied_message = 'Access is denied!'


class ProductReviewCreateView(LoginRequiredMixin, CreateView):
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


class ReviewUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    template_name = 'review/review_update.html'
    fields = ['text', 'rating']
    context_object_name = 'review'
    permission_required = 'webapp.change_review'
    permission_denied_message = 'Access is denied!'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})

    def test_func(self, **kwargs):
        review_pk = self.kwargs.get('pk')
        review = Review.objects.get(pk=review_pk)
        if self.request.user == review.author or self.request.user.has_perm('webapp.change_review'):
            return True
        else:
            return False


class ReviewDeleteView(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    context_object_name = 'review'
    template_name = 'review/review_delete.html'
    permission_required = 'webapp.delete_review'
    permission_denied_message = 'Access is denied!'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.product.pk})

    def test_func(self):
        review_pk = self.kwargs.get('pk')
        review = Review.objects.get(pk=review_pk)
        if self.request.user == review.author or self.request.user.has_perm('webapp.delete_review'):
            return True
        else:
            False