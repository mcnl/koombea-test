import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from .models import Page, Link


@pytest.mark.django_db
def test_user_signup():
    client = Client()
    signup_url = reverse("signup")
    response = client.post(
        signup_url,
        {
            "username": "testuser@koombea.com",
            "password1": "password123",
            "password2": "password123",
        },
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_login():
    user = User.objects.create_user(
        username="testuser@koombea.com", password="password123"
    )
    client = Client()
    login_url = reverse("login")
    response = client.post(
        login_url, {"username": "testuser@koombea.com", "password": "password123"}
    )
    assert response.status_code == 302  # Redirect after successful login
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_add_page():
    user = User.objects.create_user(
        username="testuser@koombea.com", password="password123"
    )
    client = Client()
    client.login(username="testuser@koombea.com", password="password123")
    add_page_url = reverse("add_page")
    response = client.post(add_page_url, {"link": "https://example.com"})
    assert response.status_code == 302  # Redirect after adding a page
    assert Page.objects.filter(user=user, page_link="https://example.com").exists()


@pytest.mark.django_db
def test_list_pages():
    user = User.objects.create_user(
        username="testuser@koombea.com", password="password123"
    )
    Page.objects.create(
        user=user, name="Test Page", page_link="https://example.com", total_links=5
    )
    client = Client()
    client.login(username="testuser@koombea.com", password="password123")
    add_page_url = reverse("add_page")
    response = client.get(add_page_url)
    assert response.status_code == 200
    assert "Test Page" in response.content.decode()


@pytest.mark.django_db
def test_page_details():
    user = User.objects.create_user(
        username="testuser@koombea.com", password="password123"
    )
    page = Page.objects.create(
        user=user, name="Test Page", page_link="https://example.com", total_links=5
    )
    Link.objects.create(page=page, name="Example Link", link="https://example.com/link")
    client = Client()
    client.login(username="testuser@koombea.com", password="password123")
    page_detail_url = reverse("page_detail", kwargs={"pk": page.pk})
    response = client.get(page_detail_url)
    assert response.status_code == 200
    assert "Example Link" in response.content.decode()
