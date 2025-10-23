import pytest

from accounts.serializers.auth_serializers import UserRegisterSerializer
from accounts.models import User

@pytest.mark.django_db
class TestUserRegisterSerializer:
    def test_valid_data(self,create_test_image):
        data ={
            "username":"newuser",
            "first_name":"New",
            "last_name":"User",
            "email":"newuser@example.com",
            "password":"Test123!",
            "phone_number":"1234567890",
            "profile_pic": create_test_image()
        }
        serializer = UserRegisterSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.username == "newuser"
        assert user.email == "newuser@example.com"
        assert user.check_password("Test123!")
        
    def test_invalid_password(self,create_test_image,user):
        data ={
            "username":"newuser",
            "first_name":"New",
            "last_name":"User",
            "email":"newuser@example.com",
            "password":"test123!",   #change Test123! to test123!
            "phone_number":"1234567890",
            "profile_pic": create_test_image()
        }
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "Password must contain at least one uppercase letter" in str(serializer.errors)
        # assert "Password must contain at least one special character" in str(serializer.errors)
        
    def test_duplicate_email(self,create_test_image):
        User.objects.create_user(username="existing",email="test@example.com",password="Test123!")
        data ={
            "username":"newuser",
            "first_name":"New",
            "last_name":"User",
            "email":"test@example.com",
            "password":"Test123!",
            "phone_number":"1234567890",
            "profile_pic": create_test_image()
        }
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "A user with this email already exists" in str(serializer.errors)

    def test_duplicate_username(self,create_test_image):
        User.objects.create_user(username="existing",email="test@example.com",password="Test123!")
        data ={
            "username":"existing",
            "first_name":"New",
            "last_name":"User",
            "email":"newuser@example.com",
            "password":"Test123!",
            "phone_number":"1234567890",
            "profile_pic": create_test_image()
        }
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "A user with this username already exists" in str(serializer.errors)