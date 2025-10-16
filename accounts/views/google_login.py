# import logging
# import uuid
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.generics import GenericAPIView
# from django.contrib.auth.base_user import BaseUserManager
# from django.contrib.auth.hashers import make_password
# from rest_framework.response import Response
# from rest_framework import status
# from django.db import transaction
# from rest_framework.permissions import AllowAny
# from google.oauth2 import id_token
# from google.auth.transport.requests import Request
# import secrets

# from serializers import UserInfoSerializer ,GoogleAuthResponseSerializer 
# from models import User

# logger = logging.getLogger(__file__)

# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return {
#         "refresh": str(refresh),
#         "access": str(refresh.access_token),
#     }

# def create_username(email):
#     try:
#         total_retries = 5
#         email_split = email.rsplit("@", 1)
#         email_part = email_split[0][:20]
#         clean_email_part = "".join(char for char in email_part if char.isalnum())
#         for i in range(total_retries):
#             uuid1 = str(uuid.uuid4())[:3]
#             username = f"{clean_email_part}_{uuid1}".lower()
#             if not User.objects.filter(username=username).exists():
#                 return username
#         raise Exception("Max retries done for creating a new username.")
#     except Exception as e:
#         raise Exception("Error while creating a new username") from e
    
# def make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789!@#$%&'):
#     return ''.join(secrets.choice(allowed_chars) for i in range(length))

# class GoogleAuthView(GenericAPIView):
#     permission_classes = [AllowAny]
#     response_serializer_class = UserInfoSerializer

#     def post(self, request):
#         try:
#             token = request.data.get('token')
#             if not token:
#                 logger.error("No Google token provided", exc_info=True)
#                 return Response({
#                     "status": "error",
#                     "message": "Google token is required",
#                     "payload": {}
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             # Verify Google ID token
#             idinfo = id_token.verify_oauth2_token(
#                 token,
#                 Request(),
#                 '769612076942-necd30n6nv8jo5sn3hcenkmuljnq7rbt.apps.googleusercontent.com',
#             )
#             logger.info("Google ID token verified", extra={"idinfo": idinfo})
#             print(idinfo)
#             # Extract user data from ID token
#             email = idinfo.get('email', '').lower()
#             given_name = idinfo.get('given_name', '')
#             family_name = idinfo.get('family_name', '')

#             # Verify the audience (client ID)
#             if idinfo.get('aud') != '769612076942-necd30n6nv8jo5sn3hcenkmuljnq7rbt.apps.googleusercontent.com':
#                 logger.error("Invalid audience in Google token", exc_info=True)
#                 return Response({
#                     "status": "error",
#                     "message": "Invalid token audience",
#                     "payload": {}
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             # Create or update user
#             is_new_user = False
#             with transaction.atomic():
#                 user = User.objects.filter(email=email).first()
#                 if user is None:
#                     print("user niiiiiiiiiiiiiiiiiiist")
#                     is_new_user = True
#                     username = create_username(email)
#                     password = make_random_password()
#                     user = User.objects.create_user(
#                         username=username,
#                         password=password,
#                         email=email,
#                         first_name=given_name,
#                         last_name=family_name,
#                         is_email_verified=True,
#                         )
#                     serializer_data = self.response_serializer_class(user, context={"request": request})
#                     return Response(
#                         data={
#                             "status": "success",
#                             "message": "Login and Create User Successful",
#                             "payload": serializer_data.data,
#                             "token": get_tokens_for_user(user),
#                         },
#                         status=status.HTTP_201_CREATED,
#                     )
#                 if not user.is_active:
#                     user.is_active = True
#                     user.save()

#             serializer_data = self.response_serializer_class(user, context={"request": request})
#             return Response(
#                 data={
#                     "status": "success",
#                     "message": "Login Successful",
#                     "payload": serializer_data.data,
#                     "token": get_tokens_for_user(user),
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         except ValueError as e:
#             logger.error(f"Invalid Google token: {str(e)}", exc_info=True)
#             return Response({
#                 "status": "error",
#                 "message": "Wrong google token / this google token is already expired.",
#                 "payload": {}
#             }, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             logger.error(f"Unexpected error during Google auth: {str(e)}", exc_info=True)
#             return Response({
#                 "status": "error",
#                 "message": "Unexpected error occurred, contact support for more info",
#                 "payload": {}
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)