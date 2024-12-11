from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from courses.models import Course, Lesson

User = get_user_model()

class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test_email@test.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(name='Test Course', owner=self.user)

        self.lesson_data = {
            'course': self.course.id,
            'title': 'Test Lesson',
            'video_url': 'https://www.youtube.com/watch?v=example'
        }

    def test_lesson_create(self):
        url = reverse('courses:lesson_create')
        response = self.client.post(url, data=self.lesson_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.first().title, 'Test Lesson')

    def test_lesson_list(self):
        url = reverse('courses:lesson_list')
        Lesson.objects.create(course=self.course, title='Lesson 1', owner=self.user)
        Lesson.objects.create(course=self.course, title='Lesson 2', owner=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_lesson_retrieve(self):
        lesson = Lesson.objects.create(course=self.course, title='Test Lesson', owner=self.user)

        url = reverse('courses:lesson_detail', args=(lesson.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Lesson')

    def test_lesson_update(self):
        lesson = Lesson.objects.create(course=self.course, title='Test Lesson', owner=self.user)
        url = reverse('courses:lesson_update', args=(lesson.id,))
        updated_data = {
            'course': self.course.id,
            'title': 'Updated Lesson',
            'video_url': 'https://www.youtube.com/watch?v=updated'
        }

        response = self.client.put(url, data=updated_data)

        print("Response status code:", response.status_code)
        print("Response data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Lesson')

    def test_lesson_partial_update(self):
        lesson = Lesson.objects.create(course=self.course, title='Test Lesson', owner=self.user)
        url = reverse('courses:lesson_update', args=(lesson.id,))
        updated_data = {
            'title': 'Updated Lesson',
            'video_url': 'https://www.youtube.com/watch?v=updated'
        }

        response = self.client.patch(url, data=updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Lesson')

    def test_lesson_delete(self):
        lesson = Lesson.objects.create(course=self.course, title='Test Lesson', owner=self.user)
        url = reverse('courses:lesson_delete', args=(lesson.id,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)
