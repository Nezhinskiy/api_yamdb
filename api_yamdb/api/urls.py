from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', views.UserViewSet, basename='user')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comment'
)
router_v1.register(r'categories', views.CategoryViewSet, basename='category')
router_v1.register(r'genres', views.GenreViewSet, basename='genre')
router_v1.register(r'titles', views.TitleViewSet, basename='title')

urlpatterns = [
    path('v1/auth/signup/', views.SignUpView.as_view(), name='auth_signup'),
    path('v1/auth/token/', views.GetTokenView.as_view(), name='auth_token'),
    path('v1/users/me/', views.CurrentUserView.as_view(), name='current_user'),
    path('v1/', include(router_v1.urls)),
]
