from django.urls import path
from .views import UserByMetadataView, ProductListView, CheckoutView

urlpatterns = [
    path('user/by-meta/<str:meta_key>/<str:meta_value>/', UserByMetadataView.as_view(), name='user-by-metadata'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]