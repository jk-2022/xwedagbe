from django.urls import path
from .views import TypeListCreateAPIView, TypeRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', TypeListCreateAPIView.as_view(), name="type-list"),
    path('<int:pk>/', TypeRetrieveUpdateDestroyAPIView.as_view(), name="type-delete"),
]