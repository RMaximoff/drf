from rest_framework import viewsets, generics, filters
from rest_framework.viewsets import ModelViewSet

from apps.courses.models import Course, Lesson, Payments
from apps.courses.permission import IsOwnerOrStaff
from apps.courses.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrStaff]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

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
    permission_classes = [IsOwnerOrStaff]
    serializer_class = LessonSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsOwnerOrStaff]
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsOwnerOrStaff]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsOwnerOrStaff]
    serializer_class = LessonSerializer


class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsOwnerOrStaff]
    queryset = Lesson.objects.all()


class PaymentsViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrStaff]
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['date_payment']
    search_fields = ['course__title', 'lesson__title', 'payment_type']

