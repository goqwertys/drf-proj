from django.contrib import admin

from courses.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'preview',
        'amount',
        'changed_at',
        'created_at',
        'owner',
        'owner',
    )
    list_filter = (
        'owner',
    )
    search_fields = (
        'name',
        'description',
        'owner',
    )
    ordering = (
        '-changed_at', 'created_at'
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'course',
        'title',
        'preview',
        'video_url',
        'amount',
        'changed_at',
        'created_at',
        'owner',
        'owner',
    )
    list_filter = (
        'owner',
        'course'
    )
    search_fields = (
        'title',
        'description',
        'owner'
    )
