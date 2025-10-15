from rest_framework import serializers

class GoogleAuthResponseSerializer(serializers.Serializer):
    sub = serializers.CharField()
    email = serializers.EmailField()
    email_verified = serializers.BooleanField()
    name = serializers.CharField()
    given_name = serializers.CharField()
    family_name = serializers.CharField(required=False)