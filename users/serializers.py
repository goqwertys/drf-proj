from rest_framework import serializers

from courses.serializers import CourseSerializer, LessonSerializer
from users.models import Payment, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'phone_number', 'city', 'avatar', 'date_joined']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class PaymentSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    lesson = serializers.SerializerMethodField()

    def get_course(self, obj):
        if obj.course:
            return CourseSerializer(obj.course).data
        return None

    def get_lesson(self, obj):
        if obj.lesson:
            return LessonSerializer(obj.lesson).data
        return None

    class Meta:
        model = Payment
        fields = ['user', 'date', 'course', 'lesson', 'amount', 'method']
