from django.urls import path

from .apps import ProductsConfig
from . import views

app_name = ProductsConfig.name


urlpatterns = [
    path('products/', views.ProductTemplateView.as_view(), name='products')
]
