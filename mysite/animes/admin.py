# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AnimeWork, Review, User


class AnimeWorkAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Anime Basic Info', {'fields' : ['anime_id', 'anime_name', 'anime_description']}),
        ('Anime Detail Info', {'fields' : ['anime_avatar_url', 'anime_cover_image_url', 'anime_rating', ]}),
    ]

# class AnimeUserInline(admin.StackedInline):
#     model = AnimeUser
#     can_delete = False
#     verbose_name_plural = 'AnimeUser'
#
# class AnimeUserAdmin(BaseUserAdmin):
#     inlines = (AnimeUserInline,)

admin.site.register(AnimeWork, AnimeWorkAdmin)
admin.site.register(Review)

admin.site.register(User, UserAdmin)
