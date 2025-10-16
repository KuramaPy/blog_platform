from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import User

class EmailViewset(viewsets.ViewSet):
    
    permission_classes=[AllowAny]
    @action(detail=False, methods=['get'])
    def verify(self,request):
        token = request.query_param.get('token')
        
        if not token:
            return Response(
                {
                    'message':'Token required'
                },
                status=400
            )
        try:
          user = User.objects.get(email_verification_token=token)
          user.is_email_verified=True
          user.save()
          
          return Response(
              {
                  'message':'Email Verify successfully!'
              },status=200
          )
        except User.DoesNotExist:
          return Response(
              {
                  'error':'Email not verify'
              },status=400
          )