from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path,include

from .views import AuthViewset,EmailViewset,PasswordViewset,TwoFAViewset,UserInfoViewset,UserProfileViewset,UserListViewset

router = DefaultRouter()

router.register(r'auth',AuthViewset,basename='auth')
router.register(r'email',EmailViewset,basename='email')
router.register(r'password',PasswordViewset,basename='password')
router.register(r'TwoFa',TwoFAViewset,basename='TwoFa')
router.register(r'userInfo',UserInfoViewset,basename='user_info')
router.register(r'userProfile',UserProfileViewset,basename='user_profile')
router.register(r'userList',UserListViewset,basename='user_list')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]