from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Question, Choice, AnimeWork

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

admin.site.register(Question, QuestionAdmin)
admin.site.register(AnimeWork, AnimeWorkAdmin)
