from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from chat.models import Thread, Message
from chat.serializers import ThreadSerializer, MessageSerializer


class UserRegistrationViewTestCase(APITestCase):
    url = reverse('user_register')

    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'password2': 'testpassword'
        }
        self.invalid_payload = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'password2': 'differentpassword'
        }

    def test_create_valid_user(self):
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

    def test_create_invalid_user(self):
        response = self.client.post(self.url, self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ThreadListCreateViewTestCase(APITestCase):
    url = reverse('threads_list_create')

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='testuser1', email='testuser1@example.com', password='testpass123')
        self.user2 = User.objects.create_user(username='testuser2', email='testuser2@example.com', password='testpass123')
        self.thread_payload = {
            'participants': [self.user1.id, self.user2.id]
        }

    def test_thread_create_view(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.url, self.thread_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Thread.objects.count(), 1)

    def test_create_thread_invalid_payload(self):
        self.client.force_authenticate(user=self.user1)
        invalid_payload = {
            'participants': [self.user1.id]
        }
        response = self.client.post(self.url, invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_thread_list_view(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ThreadUpdateDeleteViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.user3 = User.objects.create_user(username='user3', password='pass123')
        self.thread = Thread.objects.create()
        self.thread.participants.add(self.user1, self.user2)

    def test_thread_update_view(self):
        self.client.force_authenticate(self.user1)
        data = {
            'participants': [self.user1.id, self.user3.id]
        }
        response = self.client.put(reverse('threads_update_delete', kwargs={'pk': self.thread.pk}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Thread.objects.get(pk=self.thread.pk).participants.count(), 2)

    def test_thread_delete_view(self):
        self.client.force_authenticate(self.user1)
        response = self.client.delete((reverse('threads_update_delete', kwargs={'pk': self.thread.pk})))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Thread.objects.count(), 0)


class MessageListCreateViewTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.thread = Thread.objects.create()
        self.thread.participants.add(self.user1, self.user2)

    def test_get_messages_for_existing_thread(self):
        self.client.force_authenticate(self.user1)
        url = reverse('messages_list_create', kwargs={'thread_id': self.thread.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_message_for_existing_thread(self):
        self.client.force_authenticate(self.user1)
        url = reverse('messages_list_create', kwargs={'thread_id': self.thread.id})
        data = {'text': 'Test message'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().text, 'Test message')

    def test_create_message_for_nonexisting_thread(self):
        self.client.force_authenticate(self.user1)
        url = reverse('messages_list_create', kwargs={'thread_id': 123})
        data = {'text': 'Test message'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MessageReadViewTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.thread = Thread.objects.create()
        self.thread.participants.add(self.user1, self.user2)
        self.message = Message.objects.create(sender=self.user1, thread=self.thread, text="test message")

    def test_read_message(self):
        self.client.force_authenticate(self.user2)
        response = self.client.get(reverse('message_read', kwargs={'thread_id': self.thread.id, 'pk': self.message.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('is_read', False))
        self.assertEqual(response.data.get('sender'), self.user1.id)

    def test_read_message_by_sender(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('message_read', kwargs={'thread_id': self.thread.id, 'pk': self.message.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get('is_read', False))
        self.assertEqual(response.data.get('sender'), self.user1.id)

    def test_read_message_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('message_read', kwargs={'thread_id': self.thread.id, 'pk': self.message.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data.get('is_read', False))
        self.assertIsNone(response.data.get('sender'))











