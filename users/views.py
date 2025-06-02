from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import DemandeDemarcheurSerializer, UserRegisterSerializer, UserLoginSerializer, CustomTokenObtainPairSerializer, UserSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

class UserStatutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "is_demarcheur": user.is_demarcheur,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        })
    
class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Inscription réussie"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return Response({
                "user": {
                    "id": user.id,
                    "phone_number": user.phone_number,
                    "full_name": user.full_name,
                    "is_demarcheur": user.is_demarcheur
                },
                "tokens": tokens
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class DemandeDemarcheurView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DemandeDemarcheurSerializer(
            instance=request.user,
            data={'demande_demarcheur': True},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Demande envoyée avec succès.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)