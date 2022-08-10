from django.contrib import admin

from reviews.models import Comment, Review


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    pass
