from rest_framework import serializers
from models import User

class TwoFASerializer(serializers.ModelSerializer):
    TwoFA_is_enable = serializers.BooleanField()
    otp = serializers.CharField(max_length=6 ,min_length=6, required=False)
    
    class Meta:
        model = User
        fileds = [
            'TwoFA_is_enable','otp'
        ]
        
    def update(self,instance,validated_data):
        instance.gfa_is_enabled = validated_data.get('TwoFA_is_enable',instance.gfa_is_enabled)
        instance.save()
        return instance