# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Question, Choice, AnimeWork, Review, User

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields' : ['question_text']}),
        ('Date information', {'fields' : ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date', 'question_text']
    search_fields = ['question_text']

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

admin.site.register(Question, QuestionAdmin)
admin.site.register(AnimeWork, AnimeWorkAdmin)
admin.site.register(Review)

admin.site.register(User, UserAdmin)
