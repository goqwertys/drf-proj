from rest_framework import serializers

from courses.models import Course, Lesson, Subscription
from courses.validators import NoExternalLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [NoExternalLinkValidator(fields=['video_url'])]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    id_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, instance):
        return instance.lessons.count()

    def get_id_subscribed(self, instance):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(
                user=user,
                course=instance,
                is_active=True
            ).exists()
        return False

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'preview',
            'lesson_count',
            'lessons',
            'owner',
            'id_subscribed'
        ]
        validators = [NoExternalLinkValidator(fields='description')]
