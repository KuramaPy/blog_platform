from rest_framework import serializers
from models import User

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    profile_pic = serializers.ImageField()
    avatar = serializers.ImageField()
    bio = serializers.CharField()
    location = serializers.CharField()
    website = serializers.URLField()
    social_links = serializers.URLField()
    
    
    class Meta:
        model = User
        
        fields = [
            'username', 'email', 'first_name', 'last_name', 'phone_number', 'birthdate','gfa_is_enabled','profile_pic','avatar'
        ]
        
        read_only_fields= [
            'username',
        ]
        
    def validate_email(self,data):
        email = data.get('email')
        
        if email and User.objects.filter(email=email).exclude(pk=self.instance.user.pk).exists():
            raise serializers.ValidationError({'eamil':'This email is choosen Before.'})
        
        return data
    
    def update(self, instance, validated_data):
        
        new_email = validated_data.get('eamil',instance.email)
        
        if new_email != instance.email:
            instance.is_email_verified = False
            
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)        
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.profile_pic = validated_data.get('profile_pic',instance.profile_pic)
        instance.avatar = validated_data.get('avatar',instance.avatar)
        instance.save()
        
        return instance