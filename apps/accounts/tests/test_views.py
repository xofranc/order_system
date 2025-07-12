from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        
    def test_user_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("profile")}')
        
    def test_profile_view_authenticated(self):
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')
        self.assertContains(response, 'User')

    def test_update_profile_view_get(self):
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(reverse('update_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="Test"')  # Campo first_name cargado

    def test_update_profile_view_post(self):
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.post(reverse('update_profile'), {
            'first_name': 'NuevoNombre',
            'last_name': 'Actualizado',
            'email': 'nuevo@email.com'
        })
        self.assertRedirects(response, reverse('profile'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'NuevoNombre')
        self.assertEqual(self.user.last_name, 'Actualizado')
        self.assertEqual(self.user.email, 'nuevo@email.com')
