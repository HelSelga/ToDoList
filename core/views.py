from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.models import User
from core.serializers import UserRegistrationSerializer, UserLoginSerializer, UserDetailSerializer, \
    UpdatePasswordSerializer


class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class LoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            serializer_ = UserDetailSerializer(user)
            return JsonResponse(serializer_.data, safe=False)
        else:
            raise ValidationError("Невозможно отобразить данные пользователя!")


@method_decorator(ensure_csrf_cookie, name="dispatch")
class ProfileView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user

    def destroy(self, request):
        logout(request)
        return redirect("/core/login/", status=204)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class UpdatePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        return self.request.user
