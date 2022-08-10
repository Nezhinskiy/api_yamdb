from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Comment, Review

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
        user.generate_confirmation_code()
        user.save()
        user.send_confirmation_code()
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.IntegerField()

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
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
        slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review_id',)
