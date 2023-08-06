from django.core.management import BaseCommand

from apps.courses.models import Course, Lesson, Payments
from apps.users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        Course.objects.all().delete()
        User.objects.all().delete()
        Lesson.objects.all().delete()
        Payments.objects.all().delete()

        user1 = User.objects.create(email='user1@example.com', phone='1234567890', city='City 1')
        user2 = User.objects.create(email='user2@example.com', phone='9876543210', city='City 2')

        course1 = Course.objects.create(title='Course 1', description='Description 1', preview='course/preview1.jpg')
        course2 = Course.objects.create(title='Course 2', description='Description 2', preview='course/preview2.jpg')

        lesson1 = Lesson.objects.create(title='Lesson 1', description='Lesson Description 1', preview='lesson/preview1.jpg', video_link='https://example.com/video1', course=course1)
        lesson2 = Lesson.objects.create(title='Lesson 2', description='Lesson Description 2', preview='lesson/preview2.jpg', video_link='https://example.com/video2', course=course2)

        payment1 = Payments.objects.create(user=user1, course=course1, lesson=lesson1, payment_amount=100.0, payment_type='cash')
        payment2 = Payments.objects.create(user=user2, course=course2, lesson=lesson2, payment_amount=200.0, payment_type='transfer')
