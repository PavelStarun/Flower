from django.urls import path
from .views import UserRegisterView, CustomLoginView, profile_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
