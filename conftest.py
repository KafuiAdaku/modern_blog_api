import pytest
from pytest_factoryboy import register
from core_apps.users.tests.factories import UserFactory
from core_apps.profiles.tests.factories import ProfileFactory


register(UserFactory)
register(ProfileFactory)

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

@pytest.fixture
def profile(db, profile_factory):
    """Fixture for Profile model"""
    user_profile = profile_factory.create()
    return user_profile

@pytest.fixture
def test_user(db, user_factory):
    """Fixture for User model"""
    user = user_factory.create()
    yield user

@pytest.fixture
def test_user2(db, user_factory):
    """Fixture for User model"""
    user = user_factory.create()
    yield user

@pytest.fixture
def test_profile(db, test_user):
    """Fixture for Profile model"""
    profile = ProfileFactory(user=test_user)
    yield profile

@pytest.fixture
def test_profile2(db, test_user2):
    """Fixture for Profile model"""
    profile = ProfileFactory(user=test_user2)
    yield profile