from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import register_view, UserDetailView, UserInfoChangeView, UserPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/update/', UserInfoChangeView.as_view(), name='user_update'),
    path('<int:pk>/password_change/', UserPasswordChangeView.as_view(), name='user_password_change')
]