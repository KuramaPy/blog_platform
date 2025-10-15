from rest_framework import serializers
from models import User

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'is_email_verified', 
            'is_active', 'is_staff', 'is_superuser', 'is_admin', 'date_joined','profile_pic','avatar',
        ]
        read_only_fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'is_email_verified',
            'is_active', 'is_staff', 'is_superuser', 'is_admin', 'date_joined','profile_pic','avatar',
        ]