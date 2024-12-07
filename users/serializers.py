from rest_framework import serializers
from django.contrib.auth import get_user_model

from courses.serializers import CourseSerializer, LessonSerializer
from users.models import Payment

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number', 'city', 'avatar']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', None),
            city=validated_data.get('city', None),
            avatar=validated_data.get('avatar', None)
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'city', 'avatar']
        read_only_fields = ['id']


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
