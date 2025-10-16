from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..serializers import UserInfoSerializer


class UserInfoViewset(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer
    
    def get_object(self):
        return self.request.user
    
    @action(detail=False,methods=['get'])
    def get_info(self,request):
        try:
            user = self.get_object()
            serializer = self.get_serializer(user)
            return Response( serializer.data, status=200)
        except Exception as e:
            return Response( {'error':str(e)}, status=400)
        