import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


@pytest.mark.django_db
class TestAuthViews:
    
    def test_resgister_success(self, api_client , create_test_image):
        data = {
            "username":"newuser",
            "first_name":"New",
            "last_name":"User",
            "email":"newuser@example.com",
            "password":"Test123!",
            "phone_number":"1234567890",
            "profile_pic": create_test_image()
        }
        
        response = api_client.post(reverse("auth-register"), data, format='multipart')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "User registered succesfully"
        assert User.objects.filter(username="newuser").exists()
        
    def test_login_success(self, api_client,user):
        data = {
            "username":"testuser",
            "password":"Test123!"
        }
        response = api_client.post(reverse("auth-login"),data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['username']=="testuser"
        
    def test_login_invalid_credentials(self,api_client):
        data = {
            "username":"wronguser",
            "password":"wrongpasswortd"
        }
        response = api_client.post(reverse("auth-login"),data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Invalid Username and Password" 
        
    def test_logout_success(self, api_client, user):
        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
        data = {"refresh": str(refresh)}
        response = api_client.post(reverse("auth-logout"), data)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["message"] == "logout successfully"

    def test_logout_no_refresh_token(self, api_client, user):
        api_client.force_authenticate(user=user)
        response = api_client.post(reverse("auth-logout"), {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["message"] == "Refresh Token Required"