from django.urls import path
from .views import ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView, ProductCreateView

urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name="location-list"),
    path('create/', ProductCreateView.as_view(), name="location-create"),
    path('<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name="location-detail"),
]