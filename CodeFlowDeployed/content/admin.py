from django.contrib import admin
from CodeFlowDeployed.content.models import Question, Lecture, Section


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_at', 'is_answered')
    search_fields = ('title', 'author', 'is_answered')
    ordering = ('pk', 'author', 'created_at', 'is_answered')
    readonly_fields = ('slug', 'pk')
    list_filter = ('is_answered', 'created_at')


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_at')
    search_fields = ('title', 'author')
    ordering = ('pk', 'author', 'created_at')
    readonly_fields = ('slug', 'pk')
    list_filter = ('title', 'created_at')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'text', 'lecture',)
    search_fields = ('section_name', 'lecture',)
    ordering = ('pk', 'section_name', 'lecture',)
    list_filter = ('lecture', )
    readonly_fields = ('pk', 'lecture')