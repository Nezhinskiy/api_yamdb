from django.contrib import admin

from reviews.models import Comments, Reviews


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    pass


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass
