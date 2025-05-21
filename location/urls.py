from django.urls import path
from .views import ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView, ProductCreateView, MesProductsAPIView, UpdateProductStatusAPIView

urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name="location-list"),
    path('create/', ProductCreateView.as_view(), name="location-create"),
    path('<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name="location-detail"),
    path('me/', MesProductsAPIView.as_view(), name="my-products"),
    path('update-status/<int:pk>/', UpdateProductStatusAPIView.as_view(), name="location-status"),
]