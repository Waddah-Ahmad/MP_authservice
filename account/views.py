import json
from lib2to3.pgen2 import token
from tokenize import group
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import AddStreamer, SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken,BlacklistedToken,OutstandingToken,AccessToken


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_admin'] = user.is_admin
        token['email'] = user.email
        token['is_streamer'] = user.is_streamer
        token['group'] = user.group
        return token


def get_tokens_for_user(user):
    refresh = CustomTokenObtainPairSerializer.get_token(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class AddStreamerView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAdminUser]

  def post(self, request, format=None):
    serializer = AddStreamer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return Response("Streamer Added Sucessfully...", status=status.HTTP_201_CREATED)


class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]

  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token['access'],'msg':'Registered'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
  renderer_classes = [UserRenderer]

  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token': token['access'],'refresh':token['refresh'], 'msg': 'Password '}, status=status.HTTP_200_OK)
    else:
      return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class AdminLoginView(APIView):
  renderer_classes = [UserRenderer]

  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    group = serializer.data.get('group')
    user = authenticate(email=email, password=password,group=group)
    if user is not None:
      # if group !="user":
          if (group =="admin" or user.is_admin): 
            token = get_tokens_for_user(user)
            return Response({'token': token['access'], 'msg': 'Password '}, status=status.HTTP_200_OK)
          else:
            return Response({'errors': {'non_field_errors': ['Not admin']}}, status=status.HTTP_403_FORBIDDEN)
      # else:
      #   return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    else:
      return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class StreamerLoginView(APIView):
  renderer_classes = [UserRenderer]

  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    group = serializer.data.get('group')
    user = authenticate(email=email, password=password,group=group)
    if user is not None:
        if (group =="streamer" or user.is_streamer): 
          token = get_tokens_for_user(user)
          return Response({'token': token['access'], 'msg': 'Password '}, status=status.HTTP_200_OK)
        else:
          return Response({'errors':{'non_field_errors':['Not Streamer']}},status=status.HTTP_403_FORBIDDEN)
    else:
      return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]

  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]

  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]

  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg': 'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]

  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)

# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         try:
#             access_token = request.data["access"]
#             token = AccessToken(access_token)
#             token.blacklist()

#             return Response({'msg':'Logged Out Successfully'},status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({'msg':'Cannot Log Out'},status=status.HTTP_400_BAD_REQUEST)

class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response({'msg':'Logged out all'},status=status.HTTP_205_RESET_CONTENT)