from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.registerOrganization.as_view(), name='register-organization'),
    path('login/', views.LoginOrganization.as_view(), name='login-organization'),
    path('products/', views.addProducts.as_view(), name='add-products'),
]