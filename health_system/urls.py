from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import dashboard
from accounts.views import CustomLoginView, RegisterView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')), 
    path('', dashboard, name='dashboard'),
    # path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('clients/', include('clients.urls')),
    path('programs/', include('programs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
if settings.DEBUG:
    urlpatterns += [
        path('metrics/', include('django_prometheus.urls')),
    ]
