from rest_framework import serializers

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    
class PasswordChangeSerializer(serializers.Serializer):
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    def validate_password(self,value):
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char in "!@#$%^&*" for char in value):
            raise serializers.ValidationError("Password must contain at least one special character (!@#$%^&*).")
        
        return value