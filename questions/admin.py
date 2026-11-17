from django.contrib import admin
from .models import Question, Answer, Tag, QuestionLike, AnswerLike

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0
    raw_id_fields = ('user',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'title', 'text', 'likes', 'number_of_answers']
    raw_id_fields = ('user',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'text')
    list_select_related = ('user',)
    inlines = [AnswerInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'question', 'text', 'likes', 'best_answer']
    raw_id_fields = ('user', 'question')
    list_filter = ('best_answer',)
    search_fields = ('question__title', 'text')
    list_select_related = ('user', 'question')

@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'question', 'like_or_dislike']
    raw_id_fields = ('user', 'question')
    list_filter = ('like_or_dislike',)
    search_fields = ('question__title', 'user__username')
    list_select_related = ('user', 'question')

@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'answer', 'like_or_dislike']
    raw_id_fields = ('user', 'answer')
    list_filter = ('like_or_dislike',)
    search_fields = ('answer__text', 'user__username')
    list_select_related = ('user', 'answer')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name_tag']
    search_fields = ('name_tag',)
