from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from serializers import UserProfileSerializer

class UserProfileViewset(viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    @action(detail=True,methods=['get'])
    def get_profile(self,request):
        
        profile = self.get_object()
        try:
            serializer = self.get_serializer(profile)
            return Response(serializer.data,status=200)
        except Exception as e:
            return Response({'error':e},status=400)
        
    @action(detail=True,methods=['patch'])
    def update_profile(self,request):
        profile = self.get_object()
        serializer = self.get_serializer(profile,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message':'profile Updated'},status=200)
    
    @action(detail=False,methods=['post'])
    def resend_email_verification(self,request):
        user = request.user
        if user.is_email_verified:
            return Response({'error':'Email Already is verified'},status=400)
        # subject = 'Verify Your Email Address'
        # message = render_to_string('emails/verification_email.html', {
        #     'user': user,
        #     'domain': settings.SITE_DOMAIN,
        #     'verification_token': user.email_verification_token
        # })
        # send_mail(
        #     subject,
        #     message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [user.email],
        #     html_message=message
        # )
        
        return Response({'message':'Verification email sent'},status=200)