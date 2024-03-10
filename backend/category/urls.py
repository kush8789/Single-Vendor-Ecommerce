from django.urls import path
from . import views

app_name= "category"

urlpatterns = [
    path('categories/', views.CategoryListCreateAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
    path('products/', views.ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductListAPIView.as_view(), name='product-list-by-category'),
]