from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import UserProfile, Post, Category

class UserRegistrationTestCase(APITestCase):
    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'role': 'editor'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

class PostAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='admin123')
        UserProfile.objects.create(user=self.admin_user, role='admin')
        
        self.editor_user = User.objects.create_user(username='editor', password='editor123')
        UserProfile.objects.create(user=self.editor_user, role='editor')
        
        self.reader_user = User.objects.create_user(username='reader', password='reader123')
        UserProfile.objects.create(user=self.reader_user, role='reader')
        
        self.category = Category.objects.create(name='Tech', description='Technology posts')
        
    def test_admin_can_create_post(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'title': 'Test Post',
            'content': 'Test content',
            'category': self.category.id,
            'status': 'published'
        }
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_reader_cannot_create_post(self):
        self.client.force_authenticate(user=self.reader_user)
        data = {
            'title': 'Test Post',
            'content': 'Test content'
        }
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_editor_can_edit_own_post(self):
        self.client.force_authenticate(user=self.editor_user)
        post = Post.objects.create(
            title='Editor Post',
            content='Content',
            author=self.editor_user,
            status='draft'
        )
        
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/posts/{post.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
