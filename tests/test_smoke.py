from django.conf import settings


def test_django_imports():
    assert settings.configured
