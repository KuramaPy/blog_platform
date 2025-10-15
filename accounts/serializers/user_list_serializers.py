from rest_framework import serializers
from models import User

class UserListSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(required = False)
    is_staff = serializers.BooleanField(required = False)
    is_active = serializers.BooleanField(required = False)
    is_email_verified = serializers.BooleanField(required = False)
    gfa_is_enabled = serializers.BooleanField(required = False)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name','is_email_verified',
            'is_staff', 'is_active', 'is_admin', 'date_joined','gfa_is_enabled',
        ]
        read_only_fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'date_joined',
        ]

    def update(self, instance, validated_data):
        instance.is_email_verified = validated_data.get('is_email_verified', instance.is_email_verified) 
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)
        instance.gfa_is_enabled = validated_data.get('gfa_is_enabled', instance.gfa_is_enabled)
        if not instance.gfa_is_enabled:
            instance.gfa_secret=None
        instance.save()

        return instance