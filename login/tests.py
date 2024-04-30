from django.test import TestCase, Client
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User as Django_User
from login.models import User, Report
from login.forms import InputForm


# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Django_User.objects.create_user(username='testuser',
                                                    email='test@example.com',
                                                    password='password123')
        self.client.force_login(self.user)
        self.home_url = reverse('login:home')

    def test_login_page_render(self):
        response = self.client.get(reverse('login:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login_page.html')
    
    def test_home_page_render(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('login:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/home_page.html')

    def test_welcome_page_render(self):
        response = self.client.get(reverse('login:welcome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/welcome_page.html')

    def test_access_anonymous(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/home_page.html')

    def test_access_admin(self):
        User.objects.create(username='testuser', email='test@example.com', is_admin=True)
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/admin_home.html')

    def test_access_user(self):
        User.objects.create(username='testuser', email='test@example.com', is_admin=False)
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/home_page.html')

    def test_access_invalid_page(self):
        invalid_url = '/invalid-page/'
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)

    def test_see_submission_view(self):
        report = Report.objects.create(full_name='Test User', incident_type='Test Incident', description='Test Description', location='Test Location')
        response = self.client.get(reverse('login:submission', args=[report.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/view_submission.html')
    
    def test_form_valid(self):
        data = {
            'full_name': 'John Doe',
            'incident_type': '1',
        }
        form = InputForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_missing_fields(self):
        data = {}
        form = InputForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_field_types(self):
        form = InputForm()
        self.assertIsInstance(form.fields['full_name'], forms.CharField)
        self.assertIsInstance(form.fields['incident_type'], forms.ChoiceField)
        self.assertIsInstance(form.fields['description'], forms.CharField)
        self.assertIsInstance(form.fields['location'], forms.CharField)
        self.assertIsInstance(form.fields['images'], forms.ImageField)
        self.assertIsInstance(form.fields['videos'], forms.FileField)
        self.assertEqual(form.fields['full_name'].max_length, 200)