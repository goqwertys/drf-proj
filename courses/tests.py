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
        lesson_1 = Lesson.objects.create(course=self.course, title='Lesson 1', owner=self.user)
        lesson_2 = Lesson.objects.create(course=self.course, title='Lesson 2', owner=self.user)

        response = self.client.get(url)
        data = response.json()

        expected_result = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": lesson_1.id,
                    "title": lesson_1.title,
                    "preview": None,
                    "video_url": None,
                    "course": self.course.id,
                    "owner": self.user.id
                },
                {
                    "id": lesson_2.id,
                    "title": lesson_2.title,
                    "preview": None,
                    "video_url": None,
                    "course": self.course.id,
                    "owner": self.user.id
                }
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], expected_result['count'])
        self.assertEqual(data['next'], expected_result['next'])
        self.assertEqual(data['previous'], expected_result['previous'])

        for i, lesson_data in enumerate(data['results']):
            self.assertEqual(lesson_data['id'], expected_result['results'][i]['id'])
            self.assertEqual(lesson_data['title'], expected_result['results'][i]['title'])
            self.assertEqual(lesson_data['preview'], expected_result['results'][i]['preview'])
            self.assertEqual(lesson_data['video_url'], expected_result['results'][i]['video_url'])
            self.assertEqual(lesson_data['course'], expected_result['results'][i]['course'])
            self.assertEqual(lesson_data['owner'], expected_result['results'][i]['owner'])

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
