from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import RegistrationSerializer, ActivationSerializer, LoginSerializer, \
    ForgotPasswordCompletelySerializer, ForgotPasswordSerializer, ChangePasswordSerializer, EditProfileSerializer, \
    ProfileSerializer, User


class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.create()

        return Response('Вы успешно зарегистрировались', status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    def post(self, request):
        data = request.data
        serializer = ActivationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response('Ваш аккаунт успешно активирован', status=status.HTTP_200_OK)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        user.auth_token.delete()
        return Response('Successfully logged out')


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data,
                                              context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Пароль успешно изменён')


class ForgotPasswordView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.send_email()
        return Response('Вам выслан код подтверждения')


class ForgotPasswordCompletelyView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordCompletelySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Вы успешно восстановили пароль')


class EditProfileView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = EditProfileSerializer



class ProfileView(APIView):
    queryser = User.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProfileSerializer