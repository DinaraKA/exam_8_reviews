from django.urls import path

from webapp.views import IndexView, ProductView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    ProductReviewCreateView, ReviewUpdateView, ReviewDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/review_add/', ProductReviewCreateView.as_view(), name='product_review_add'),
    path('review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review_update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
]