from django.urls import path
from .views import VilleListCreateAPIView, VilleRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', VilleListCreateAPIView.as_view(), name="villes-list"),
    path('<int:pk>/', VilleRetrieveUpdateDestroyAPIView.as_view(), name="villes-delete"),
]