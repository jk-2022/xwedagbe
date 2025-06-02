from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class DemandeDemarcheurSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['demande_demarcheur']

    def validate_demande_demarcheur(self, value):
        if self.instance.is_demarcheur:
            raise serializers.ValidationError("Vous êtes déjà un démarcheur.")
        return value

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'full_name', 'password', 'is_demarcheur']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
            is_demarcheur=validated_data.get('is_demarcheur', False)
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            phone_number=data.get("phone_number"),
            password=data.get("password")
        )
        if not user:
            raise serializers.ValidationError("Identifiants invalides")
        if not user.is_active:
            raise serializers.ValidationError("Utilisateur inactif")
        return {"user": user}
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["phone_number"] = user.phone_number
        return token

    def validate(self, attrs):
        self.user = CustomUser.objects.filter(phone_number=attrs.get("phone_number")).first()
        return super().validate(attrs)

    def get_fields(self):
        fields = super().get_fields()
        # Ajoute explicitement le champ phone s'il n'existe pas
        if "username" in fields:
            fields["phone_number"] = fields.pop("username")
        else:
            fields["phone_number"] = serializers.CharField()
        return fields


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "phone_number", "full_name", "is_demarcheur", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "phone_number": {"read_only": True},  # non modifiable
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance