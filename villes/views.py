from rest_framework import generics
from .models import Ville
from .serializers import VilleSerializer

class VilleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ville.objects.all()
    serializer_class = VilleSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VilleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ville.objects.all()
    serializer_class = VilleSerializer