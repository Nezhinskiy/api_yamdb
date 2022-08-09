from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import GetTokenView, SignUpView, ReviewViewSet, CommentViewSet

app_name = 'api'

api_router = DefaultRouter()

api_router.register(r'titles/(?P<title_id>\d+)/reviews',
                    ReviewViewSet, basename='reviews')
api_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='auth_signup'),
    path('v1/auth/token/', GetTokenView.as_view(), name='auth_token'),
    path('v1/auth/token/', include(api_router.urls), name='api')
]
