import pytest
import uuid

from accounts.models import User

@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="Test123!",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
        )
        
        assert user.id is not None
        assert isinstance(user.id , uuid.UUID)
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.check_password("Test123!")
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.phone_number == "1234567890"
        
    def test_user_followers(self):
        user1 = User.objects.create_user(username="user1", email="user1@example.com", password="Test123!")
        user2 = User.objects.create_user(username="user2", email="user2@example.com", password="Test123!")
        user1.followers.add(user2)
        user2.followers.add(user1)
        assert user2 in user1.followers.all()
        assert user1 in user2.followers.all()