from rest_framework import mixins,viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter , SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from models import User
from serializers import UserListSerializer
from permisions import IsSuperuserOrAdmin


class UserListViewset(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet
                      ):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [ IsAuthenticated,IsSuperuserOrAdmin]
    pagination_class = [PageNumberPagination]
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filterset_fields = ['is_staff', 'is_admin', 'is_active']
    search_fields = ['username', 'email', 'last_name']
    ordering_fields = ['is_active','date_joined','is_email_verified','is_staff','is_admin']
    ordering = ['date_joined']
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()
        if self.request.user.is_superuser:
            return User.objects.all()
        if self.request.user.is_admin:
            return User.objects.filter(is_admin=False,is_superuser=False,).exclude(id=self.request.user.id)
        return User.objects.none()