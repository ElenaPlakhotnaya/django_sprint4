from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group, User

from .models import Category, Comment, Location, Post


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
    )


class CustomUserAdmin(UserAdmin):
    change_password_form = PasswordChangeForm


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Location)
admin.site.register(Post)
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
