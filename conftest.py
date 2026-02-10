"""
Pytest configuration for Library Management System tests
"""
import pytest
from django.conf import settings


@pytest.fixture(scope='session', autouse=True)
def disable_password_validators():
    """Disable password validators for testing"""
    settings.AUTH_PASSWORD_VALIDATORS = []
