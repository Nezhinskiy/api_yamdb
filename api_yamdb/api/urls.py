from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import GetTokenView, SignUpView

app_name = 'api'

api_router = DefaultRouter()

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='auth_signup'),
    path('v1/auth/token/', GetTokenView.as_view(), name='auth_token'),
]
