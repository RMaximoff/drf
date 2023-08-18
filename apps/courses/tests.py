from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.courses.models import Course, Lesson, Subscriptions
from apps.users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.url = '/'
        self.course = Course.objects.create(title='test')
        self.user = User.objects.create(email='test@test.ru', password='1234')
        self.data = {
            'title': 'test',
            'description': 'test',
            'course': self.course,
            'owner': self.user
        }

        self.lesson = Lesson.objects.create(**self.data)
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        data = {
            'title': 'testT',
            'description': 'test',
            'course': self.course.pk,
            'owner': self.user.pk
        }
        lesson_create_url = reverse('course:lesson_create')
        response = self.client.post(lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_list_lesson(self):
        lesson_list_url = reverse('course:lesson_list')
        response = self.client.get(lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_detail_lesson(self):
        lesson_detail_url = reverse('course:lesson_detail', kwargs={'pk': self.lesson.pk})
        response = self.client.get(lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_update_lesson(self):
        lesson_update_url = reverse('course:lesson_update', kwargs={'pk': self.lesson.pk})
        new_title = 'new_title'
        data = {'title': new_title}
        response = self.client.patch(lesson_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, new_title)

    def test_delete_lesson(self):
        lesson_delete_url = reverse('course:lesson_delete', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())


class SubscriptionsTestCase(APITestCase):
    def setUp(self) -> None:
        self.course = Course.objects.create(title='test')
        self.user = User.objects.create(email='test@test.ru', password='1234')
        self.data = {
            'user': self.user,
            'course': self.course,
        }

        self.subscription = Subscriptions.objects.create(**self.data)
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        data = {
            'user': self.user.pk,
            'course': self.course.pk,
        }
        subscription_url = reverse('course:subscriptions-list')
        print(subscription_url)
        response = self.client.post(subscription_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscriptions.objects.all().count(), 2)

    def test_list_subscriptions(self):
        subscription_url = reverse('course:subscriptions-list')
        print(subscription_url)
        response = self.client.get(subscription_url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_subscription(self):
        subscription_detail_url = reverse('course:subscriptions-detail', kwargs={'pk': self.subscription.pk})
        response = self.client.get(subscription_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.subscription.user.pk)
