def test_django_imports():
    import django
    from django.conf import settings
    assert settings.configured
