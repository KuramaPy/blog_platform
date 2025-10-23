import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from PIL import Image
from django.conf import settings
from rest_framework.test import APIClient
import io
import os

User = get_user_model()

@pytest.fixture
def create_test_image():
    def _create_image():
        image = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return SimpleUploadedFile("test_image.png", img_byte_arr.read(), content_type="image/png")
    return _create_image

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@test.com',
        password='Test123!',
        first_name = 'Test',
        last_name="User",
        phone_number="1234567890"      
    )

@pytest.fixture(autouse=True)
def media_storage(tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath
    yield
    for filename in os.listdir(tmpdir.strpath):
        os.remove(os.path.join(tmpdir.strpath, filename))

@pytest.fixture
def api_client():
    return APIClient()
