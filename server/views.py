from rest_framework import viewsets
from .serializers import UserSerializer, UserViewSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UsersView(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return UserViewSerializer
        return UserSerializer

    def perform_create(self, instance):
        current_user = self.request.user
        user_exists = User.objects.filter(
            email=self.request.data['email']).first()
        if user_exists:
            raise MethodNotAllowed
        else:
            instance.save(is_active=True,
                          password=make_password(self.request.data['password']))
