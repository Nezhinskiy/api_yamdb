from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, mixins, permissions, status,
                            viewsets)
from rest_framework.response import Response
from rest_framework.views import APIView
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title

from api import serializers
from api.filters import TitleFilter
from api.permissions import (IsAdministrator, IsAdministratorOrReadOnly,
                             IsAuthorOrModeratorOrAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleReadSerializer, TitleWriteSerializer)
from api.utils import get_token_for_user

User = get_user_model()


class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        token = default_token_generator.make_token(user)
        user.send_confirmation_code(token)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {'confirmation_code': 'Неверный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(get_token_for_user(user), status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('username')
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
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        get_object_or_404(Title, id=title_id)
        queryset = Review.objects.select_related(
            'title', 'author'
        ).only('title__id', 'author__username').filter(title_id=title_id)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title_id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('review', 'author').all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        get_object_or_404(Review, id=review_id, title_id=title_id)
        queryset = Comment.objects.select_related(
            'review', 'author'
        ).only('review__id', 'review__title', 'author__username').filter(
            review_id=review_id, review__title_id=title_id
        )
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        get_object_or_404(Review, id=review_id, title_id=title_id)
        serializer.save(author=self.request.user, review_id=review_id)


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
            return TitleWriteSerializer
        return TitleReadSerializer
