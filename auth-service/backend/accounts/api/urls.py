from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UsersInfoView, SignUpViewSet, ExtendedTokenObtainPairView, ExtendedTokenVerifyView


router = DefaultRouter()
router.register(r'signup', SignUpViewSet, 'signup')

urlpatterns = [
    path('login/', ExtendedTokenObtainPairView.as_view(), name='login'),
    path('verify-token/', ExtendedTokenVerifyView.as_view(), name='verify'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh'),
    path('users-info/', UsersInfoView.as_view(), name='users-info')
]

urlpatterns += router.urls
