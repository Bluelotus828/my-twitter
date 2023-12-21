from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.api.serializers import (
    UserSerializer,
    LoginSerializer,
    SignupSerializer
)
from django.contrib.auth import (
    logout as django_logout,
    login as django_login,
    authenticate as django_authenticate,
)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# account status api
class AccountViewSet(viewsets.ViewSet):
    serializer_class = SignupSerializer
    """
    API endpoint that allows user login status to be viewed (only)
    """
    @action(methods=['GET'], detail=False)
    def login_status(self, request):
        data = {'has_logged_in': request.user.is_authenticated,
                'ip address': request.META['REMOTE_ADDR'],}
        # if logged in
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        django_logout(request)
        return Response({'has_logged_out':True})

    @action(methods=['POST'], detail=False)
    def login(self, request):
        # get username and password from request
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input",
                "errors": serializer.errors,
                # 400 coded response indicating a user error
            }, status=400)
        # validation okay then login
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # if user does not exist
        if not User.objects.filter(username=username).exists():
            return Response({
                "success": False,
                "message": "User does not exist",
                # 400 coded response indicating a user error
            }, status=400)

        user = django_authenticate(username=username, password=password)
        if not user or user.is_anonymous:
            return Response({
                "success": False,
                "message": "username and password does not match",
            }, status=400)
        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializer(instance=user).data,
        })

    @action(methods=['POST'], detail=False)
    def signup(self,request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input",
                "errors": serializer.errors,
                # 400 coded response indicating a user error
            }, status=400)

        user = serializer.save()
        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializer(user).data
        }, status=201)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        """
        登出当前用户
        """
        django_logout(request)
        return Response({"success": True})