from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {'username': 'Недопустимое имя пользователя!'}
            )
        if User.objects.filter(
            ~models.Q(email=data['email']),
            username=data['username'],
        ).exists():
            raise serializers.ValidationError(
                {'username': 'Такой пользователь уже существует!'}
            )
        if User.objects.filter(
            ~models.Q(username=data['username']),
            email=data['email']
        ).exists():
            raise serializers.ValidationError(
                {'email': 'Такой email уже существует!'}
            )
        return data

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data)
        token = default_token_generator.make_token(user)
        user.save()
        user.send_confirmation_code(token)
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
            user, data['confirmation_code']
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения!'}
            )
        return data

    def create(self, validated_data):
        return User.objects.get(username=validated_data['username'])


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='pk'
    )

    def validate(self, data):
        title = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        is_exists = Review.objects.filter(title=title, author=author)
        if self.context['request'].method != 'PATCH':
            if is_exists:
                raise ValidationError(
                    'Нельзя оставить более одного отзыва к одному произведению'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='pk'
    )

    class Meta:
        model = Comment
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')
        model = Title
