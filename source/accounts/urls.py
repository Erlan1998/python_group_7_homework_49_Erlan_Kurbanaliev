from django.urls import path
from accounts.views import register_view, UserDetailView, UserView, UserUpdateView, UserChangePasswordView
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', register_view, name='register'),
    path('accounts/index/', UserView.as_view(), name='index_accounts'),
    path('accounts/<int:id>/', UserDetailView.as_view(), name='all_accounts'),
    path('profile/', UserUpdateView.as_view(), name='update_user'),
    path('profile/change-password', UserChangePasswordView.as_view(), name='change_password'),
]