import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestRegisterView:
    def test_register_page_status_200(self, client):
        response = client.get(reverse('accounts:register'))
        assert response.status_code == 200

    def test_register_creates_user(self, client):
        client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'new@test.ru',
            'password1': 'strongpass99',
            'password2': 'strongpass99',
        })
        assert User.objects.filter(username='newuser').exists()

    def test_register_logs_in_after_success(self, client):
        response = client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'new@test.ru',
            'password1': 'strongpass99',
            'password2': 'strongpass99',
        })
        assert response.status_code == 302
        assert response['Location'] == '/'

    def test_register_duplicate_email_fails(self, client, user):
        response = client.post(reverse('accounts:register'), {
            'username': 'anotheruser',
            'email': user.email,
            'password1': 'strongpass99',
            'password2': 'strongpass99',
        })
        assert response.status_code == 200
        assert User.objects.filter(username='anotheruser').count() == 0

    def test_authenticated_user_redirected(self, auth_client):
        response = auth_client.get(reverse('accounts:register'))
        assert response.status_code == 302

    def test_template_used(self, client):
        response = client.get(reverse('accounts:register'))
        assert 'accounts/register.html' in [t.name for t in response.templates]


@pytest.mark.django_db
class TestLoginView:
    def test_login_page_status_200(self, client):
        response = client.get(reverse('login'))
        assert response.status_code == 200

    def test_login_success_redirects(self, client, user):
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'pass12345',
        })
        assert response.status_code == 302

    def test_login_wrong_password(self, client, user):
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        assert response.status_code == 200
        assert response.context['form'].errors
