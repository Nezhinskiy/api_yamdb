from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('v1/auth/signup/', views.SignUpView.as_view(), name='auth_signup'),
    path('v1/auth/token/', views.GetTokenView.as_view(), name='auth_token'),
    path('v1/users/me/', views.CurrentUserView.as_view(), name='current_user'),
    path('v1/', include(router_v1.urls)),
]