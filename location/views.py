# store/views.py
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from .models import Product, Review
from rest_framework.response import Response
from .serializers import *
from .permissions import IsDemarcheur
from habitalink.permissions import IsOwnerOrReadOnly, IsProductManager

@api_view(['GET'])
@permission_classes([AllowAny])
def user_status(request):
    return JsonResponse({
        'is_staff': request.user.is_staff,
        'is_admin': request.user.is_superuser
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def add_user_to_group(request):
    username = request.data.get('username')
    if not username:
        return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    group, created = Group.objects.get_or_create(name='product_manager')
    user.groups.add(group)
    return Response({"message": "User added to product_manager group"}, status=status.HTTP_200_OK)


class ProductListCreateAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(disponibilite=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsDemarcheur]
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MesProductsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDemarcheur]

    def get(self, request):
        products = Product.objects.filter(user=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
 
class UpdateProductStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, user=self.request.user)
        except Product.DoesNotExist:
            return Response({"detail": "Product introuvable."}, status=status.HTTP_404_NOT_FOUND)

        disponibilite = request.data.get("disponibilite")
        if disponibilite is not None:
            product.disponibilite = disponibilite
            product.save()
            return Response({"message": "Statut mis à jour avec succès."})
        
        return Response({"detail": "Champ disponibilite requis."}, status=status.HTTP_400_BAD_REQUEST)


# class ProductDelete(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# class ProductUpdateView(generics.UpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthenticated]
    
#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)
        
class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
