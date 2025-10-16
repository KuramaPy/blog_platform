from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=6, required=True)
    phone_number = serializers.CharField(required=True, write_only=True)
    birthdate = serializers.DateField(required=False, allow_null=True, write_only=True)
    profile_pic = serializers.ImageField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username', 'password', 'phone_number', 'birthdate','profile_pic']

    def validate_password(self, value):
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char in "!@#$%^&*" for char in value):
            raise serializers.ValidationError("Password must contain at least one special character (!@#$%^&*).")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    # check profile picture for real faces
    def validate_profile_pic(self,values):
        pass

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        data['username'] = self.user.username
        return data