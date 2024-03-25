import pytest
from pytest_factoryboy import register
from core_apps.users.tests.factories import UserFactory


register(UserFactory)

@pytest.fixture
def base_user(db, user_factory):
    """Fixture for User model"""
    new_user = user_factory.create()
    return new_user

@pytest.fixture
def super_user(db, user_factory):
    """Fixture for super user"""
    new_user = user_factory.create(is_staff=True, is_superuser=True)
    return new_user
