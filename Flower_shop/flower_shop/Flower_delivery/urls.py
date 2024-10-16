from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('apps.shop.urls')),
    path('users/', include('apps.users.urls')),
    path('', RedirectView.as_view(pattern_name='register', permanent=False)),
]
