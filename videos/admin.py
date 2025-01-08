from django.contrib import admin

# Register your models here.
from .models import Videos, Category, Contact, Comment, Quiz, Question, Yangi, Termin, Instrument, Kitoblar, QuizResult


@admin.register(Videos)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "publish_time", "status"]
    list_filter = ["status", "created_time", "publish_time"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish_time"
    search_fields = ["title", "body"]
    ordering = ["status", "publish_time"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    ordering = ["id"]


# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ["name"]
admin.site.register(Contact)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['disable_comments', 'activate_comments']

    def disable_comment(self, request, queryset):
        queryset.update(active=False)

    def activate_comment(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Comment, CommentAdmin)

admin.site.register(Quiz)
admin.site.register(Question)


@admin.register(Yangi)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "body"]
    list_filter = ["title", "body"]
    ordering = ["title"]


@admin.register(Termin)
class TerminAdmin(admin.ModelAdmin):
    list_display = ["title"]
    list_filter = ["title"]
    ordering = ["title"]


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ["title"]
    list_filter = ["title"]
    ordering = ["title"]


@admin.register(Kitoblar)
class KitoblarAdmin(admin.ModelAdmin):
    list_display = ["title", "body"]
    list_filter = ["title"]
    ordering = ["status"]


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'grade', 'time_spent', 'completed_at')
    list_filter = ('quiz', 'completed_at')
    search_fields = ('user__username', 'quiz__title')
