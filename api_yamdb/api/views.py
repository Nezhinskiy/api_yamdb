from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, mixins,
                            permissions, status, viewsets)
from rest_framework.response import Response
from rest_framework.views import APIView
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title

from api import serializers
from api.filters import TitleFilter
from api.permissions import (IsAdministrator, IsAuthorOrReadOnly,
                             IsAuthorOrModeratorOrAdminOrReadOnly)
from api.serializers import (CategorySerializer,
                             CommentSerializer,
                             GenreSerializer,
                             ReviewSerializer,
                             TitleSerializer,
                             TitlePostSerializer)
from api.utils import get_token_for_user

User = get_user_model()


class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(get_token_for_user(user), status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAdministrator,)
    lookup_field = 'username'


class CurrentUserView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save(role=self.request.user.role)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('title', 'author').all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('review', 'author').all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title=title, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        serializer.save(author=self.request.user, review=review)


class CategoryGenreViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = (IsAdministratorOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')
                                      ).order_by('year')
    permission_classes = (IsAdministratorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitlePostSerializer
        return TitleSerializer
