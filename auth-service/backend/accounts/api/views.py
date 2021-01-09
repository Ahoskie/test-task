import jwt

from django.utils.timezone import now
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework_simplejwt.serializers import TokenVerifySerializer

from .serializers import UserSerializer, SignUpSerializer, ExtendedTokenObtainPairSerializer
from accounts.staff_jwt_permissions import StaffOnlyJWTPermission


class UsersInfoView(APIView):
    http_method_names = ['post']
    permission_classes = [StaffOnlyJWTPermission]

    def post(self, request):
        data = request.data
        users_ids = data.get('users_ids')
        if users_ids is None:
            raise ValidationError({'users_ids': 'This field is required'})
        if type(users_ids) != list:
            raise ValidationError({'users_ids': 'This field must be a list'})

        users = User.objects.filter(id__in=users_ids).select_related('profile')
        serializer = UserSerializer(users, many=True)
        return Response({'users': serializer.data})


class SignUpViewSet(ModelViewSet):
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'The user has been successfully registered'}, status=201)
        else:
            return Response({'error': serializer.errors}, status=400)


class ExtendedTokenObtainPairView(TokenObtainPairView):
    serializer_class = ExtendedTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super(ExtendedTokenObtainPairView, self).post(request, *args, **kwargs)
        username = request.data['username']
        user = User.objects.get(username=username)
        user.last_login = now()
        user.save()
        return response


class ExtendedTokenVerifyView(TokenVerifyView):
    serializer_class = TokenVerifySerializer

    def post(self, request, *args, **kwargs):
        response = super(ExtendedTokenVerifyView, self).post(request, *args, **kwargs)
        user_payload = jwt.decode(request.data['token'], options={'verify_signature': False})
        user_id = user_payload['user_id']
        try:
            user = User.objects.select_related('profile').get(pk=user_id)
            user.profile.last_request_time = now()
            user.save()
        except User.DoesNotExist:
            pass
        return response
