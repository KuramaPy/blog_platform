from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.response import Response

import secrets

from serializers import PasswordResetSerializer ,PasswordChangeSerializer
from models import User

class PasswordViewset(viewsets.ViewSet):
    
    @action(detail=False,methods=['post'], permission_classes =[AllowAny])
    def reset(self,request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            new_password = secrets.token_urlsafe(12)
            user.set_password(new_password)
            user.save()
            
            # subject = 'Your New Password'
            # message = render_to_string('emails/password_reset_email.html', {
            #     'user': user,
            #     'new_password': new_password,
            #     'domain': settings.SITE_DOMAIN
            # })
            # send_mail(
            #     subject,
            #     message,
            #     settings.DEFAULT_FROM_EMAIL,
            #     [user.email],
            #     html_message=message
            # )
            return Response({"message": "New password sent to your email"}, status=200)
        except User.DoesNotExist:
            Response({"error": "User Not Found"}, status=404)
            
    
    @action(detail=False,methods=['post'],permission_classes=[IsAuthenticated])
    def change(self,request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error':'Enter currect password'},status=400)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message':'Password changed successfully!'},status=200)