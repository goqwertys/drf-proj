from rest_framework import serializers

from courses.models import Course, Lesson
from courses.validators import NoExternalLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [NoExternalLinkValidator(fields=['video_url'])]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'preview', 'lesson_count', 'lessons', 'owner']
        validators = [NoExternalLinkValidator(fields='description')]
