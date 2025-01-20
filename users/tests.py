from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APITestCase

from courses.models import Course
from users.models import User, Payment


class PaymentTesCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test_email@test.com',
            password='testpassword'
        )
        self.course = Course.objects.create(name='Test Course', amount=100)

    def test_create_payment_authenticated(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'course': self.course.id,
            'method': 'CRD',
            'status': 'pending'
        }

        url = reverse('users:payment-create')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.first()
        self.assertEqual(payment.user.email, 'test_email@test.com')
        self.assertEqual(payment.course.name, 'Test Course')

    def test_create_payment_unauthenticated(self):
        data = {
            'course': self.course.id,
            'method': 'CRD',
            'status': 'pending'
        }

        url = reverse('users:payment-create')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
