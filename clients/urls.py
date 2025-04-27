from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('create/', views.client_create, name='client_create'),
    path('<uuid:pk>/', views.client_detail, name='client_detail'),
    path('<uuid:pk>/update/', views.client_update, name='client_update'),
    path('<uuid:pk>/enroll/', views.client_enroll, name='client_enroll'),
]
