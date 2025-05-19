from django.urls import path
from .views import CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', CategoryListCreateAPIView.as_view(), name="cathegory-list"),
    path('<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name="cathegory-delete"),
]