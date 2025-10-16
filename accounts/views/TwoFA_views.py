from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

import pyotp
import qrcode
import base64
from io import BytesIO

from models import User
from serializers import TwoFASerializer


class TwoFAViewset(viewsets.GenericViewSet):
    
    serializer_class= TwoFASerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def twofa_qrcode(self,request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        user.gfa_secret = pyotp.random_base32()
        otp_uri = pyotp.totp.TOTP(user.gfa_secret).provisioning_uri(
            name=user.email, issuer_name="Blog"
        )
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(otp_uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
            
        # Convert QR code to base64 string
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        user.save()
        
        return Response({
                'user.gfa_secret': user.gfa_secret,
                'qr_code': f"data:image/png;base64,{qr_code_base64}",
                'otp_uri': otp_uri
            })
        
    @action(detail=False, methods=['patch'],permission_classes=[IsAuthenticated])
    def gfa_status(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        gfa_is_enabled = serializer.validated_data.get('gfa_is_enabled')
        otp = serializer.validated_data.get('otp')        
        if gfa_is_enabled:
            # Generate new 2FA secret and QR code
            user.gfa_is_enabled = True
            totp = pyotp.TOTP(user.gfa_secret)
            if totp.verify(otp):
                user.save()
                return Response({'detail': 'success'},status=200)
            else:
              return Response({'detail':'otp failed'},status=400)
        else:
            # Disable 2FA
            user.gfa_is_enabled = False
            user.gfa_secret = None
            user.save()
            return Response({
                'gfa_is_enabled': user.gfa_is_enabled,
                'message': '2FA disabled successfully'
            })

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def gfa_verify(self, request):
        user_id = request.data.get('user_id')
        otp = request.data.get('otp')
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist'}, status=400)
            
        if not user.gfa_is_enabled:
            return Response({'detail': '2FA is not enabled for this user'}, status=400)  
        totp = pyotp.TOTP(user.gfa_secret)
        if totp.verify(otp):
            # Generate JWT tokens upon successful 2FA verification
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'email': user.email,
                'username': user.username,
                'is_staff': user.is_staff,
                'is_admin': user.is_admin,
                'is_superuser': user.is_superuser,
                'is_active': user.is_active,
                'is_email_verified': user.is_email_verified,
            }, status=200)
        return Response({'detail': 'Invalid 2FA code'}, status=403)