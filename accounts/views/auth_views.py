from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers.auth_serializers import CustomTokenObtainPairSerializer, UserRegisterSerializer

class AuthViewset(viewsets.ViewSet):    
    permission_classes = [AllowAny]
    
    @action(detail=False,methods=['post'],)
    def register(self , request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        try:
            # subject = 'Welcome to Our Platform!'
            # message = render_to_string('emails/welcome_email.html', {
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
            return Response(
                {
                    'message':'User registered succesfully'
                },
                status=201
            )
        except:
            return Response(
                {
                    'message':'User registered But Email not sended'
                },
                status=200
            )
            
    @action(detail=False , methods=['post'])
    def login(self,request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            if user.gfa_is_enabled:
              # If 2FA is enabled, return user info without tokens
                return Response({
                    'user_id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'is_staff': user.is_staff,
                    'is_admin': user.is_admin,
                    'is_superuser': user.is_superuser,
                    'is_active': user.is_active,
                    'is_email_verified': user.is_email_verified,
                    'gfa_is_enabled': user.gfa_is_enabled,
                    'message': '2FA verification required'
                }, status=200)
            # If 2FA is not enabled, proceed with token generation
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
                'gfa_is_enabled': user.gfa_is_enabled
            }, status=200)
        except Exception:
            return Response({"detail": "Invalid Username and Password"}, status=400)
    
    @action(detail=False, methods=['post'],permission_classes=[IsAuthenticated])
    def logout(self,request):
        try:
            refrest_token = request.data.get('refresh')
            if not refrest_token:
                return Response(
                    {'message':'Refresh Token Required'},
                    status=401
                )
            token = RefreshToken(refrest_token)
            token.blacklist()
            return Response(
                {
                    'message':'logout successfully'
                },status=204
            )    
        except Exception as e:
          return Response({'error':str(e)},status=400)