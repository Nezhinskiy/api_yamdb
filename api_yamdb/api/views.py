from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from reviews.models import Comment, Review
from titles.models import Title

from . import serializers
from .permissions import IsAdministrator
from .utils import get_token_for_user

User = get_user_model()


class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(get_token_for_user(user),
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    queryset = Review.objects.select_related('title_id', 'author').all()
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title_id=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('review_id', 'author').all()
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title_id=title, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title_id=title, pk=review_id)
        serializer.save(author=self.request.user, review_id=review)
