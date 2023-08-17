from rest_framework import viewsets, generics, filters
from rest_framework.viewsets import ModelViewSet

from apps.courses.models import Course, Lesson, Payments, Subscriptions
from apps.courses.paginators import ViewsPaginator
from apps.courses.permission import IsOwnerOrStaff
from apps.courses.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionsSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrStaff]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = ViewsPaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        upd_course = serializer.save()


class LessonListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = LessonSerializer
    pagination_class = ViewsPaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Lesson.objects.all()


class PaymentsViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['date_payment']
    search_fields = ['course__title', 'lesson__title', 'payment_type']


class SubscriptionsViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = SubscriptionsSerializer
    queryset = Subscriptions.objects.all()

    def perform_create(self, serializer):
        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        new_subscription.save()

