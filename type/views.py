from rest_framework import generics
from .serializers import TypeSerializer
from .models import Type

class TypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TypeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer