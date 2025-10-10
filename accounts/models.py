from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    """
    
    """
    # base fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    birthdate = models.DateField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    gfa_secret = models.CharField(max_length=32 , blank=True , null=True)
    gfa_is_enabled = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profile_pic')
    avatar = models.ImageField(upload_to='avatar')
    
    # more datail for users
    bio = models.TextField(max_length=500, blank=True , null=True)
    location = models.CharField(max_length=15, blank=True)
    website = models.URLField(blank=True)
    # social fields
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    social_links = models.JSONField(default=dict, blank=True)
    # suggestion fields
    insterests = models.ManyToManyField('blog.Tag', related_name='user_interests', blank=True)
    # prefrences / securety fields 
    prefrences = models.JSONField(default=dict, blank=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.username}'s Profile"

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
        ordering = ['-date_joined']