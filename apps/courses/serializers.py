from abc import ABC

from rest_framework import serializers

from apps.courses.models import Course, Lesson, Payments, Subscriptions
from apps.courses.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(fields=['title', 'description', 'video_link'])]


class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        validators = [LinkValidator(fields=['title', 'description'])]

    def get_number_of_lessons(self, instance):
        return instance.lesson.all().count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscriptions.objects.filter(user=user, course=obj).exists()


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'


class SubscriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscriptions
        fields = '__all__'
