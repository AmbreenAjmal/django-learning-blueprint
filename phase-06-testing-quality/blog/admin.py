from django.contrib import admin
from .models import Post, Profile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published", "created_at"]
    list_filter = ["published"]
    search_fields = ["title", "content"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]
