import pytest


def test_user_str(base_user):
    """Test user string representation"""
    assert base_user.__str__() == f"{base_user.username}"

def test_user_short_name(base_user):
    """Test user short name"""
    short_name = f"{base_user.first_name}"
    assert base_user.get_short_name() == short_name

def test_user_full_name(base_user):
    """Test user full name"""
    full_name = f"{base_user.first_name} {base_user.last_name}"
    assert base_user.get_full_name() == full_name

def test_base_user_email_is_normalized(base_user):
    """Test user email is normalized"""
    assert base_user.email == base_user.email.lower()

def test_super_user_email_is_normalized(super_user):
    """Test super user email is normalized"""
    assert super_user.email == super_user.email.lower()

def test_super_user_is_not_staff(user_factory):
    """Test super user is not staff"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_staff=False, is_superuser=True)
    assert str(err.value) == "Superusers must have is_staff=True"

def test_super_user_is_not_superuser(user_factory):
    """Test super user is not superuser"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_staff=True, is_superuser=False)
    assert str(err.value) == "Superusers must have is_superuser=True"

def test_create_user_with_no_email(user_factory):
    """Test create user with no email"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None)
    assert str(err.value) == "Base User Account: An email address is required"

def test_create_user_with_no_username(user_factory):
    """Test create user with no username"""
    with pytest.raises(ValueError) as err:
        user_factory.create(username=None)
    assert str(err.value) == "Users must submit a username"

def test_create_user_with_no_firstname(user_factory):
    """Test create user with no first name"""
    with pytest.raises(ValueError) as err:
        user_factory.create(first_name=None)
    assert str(err.value) == "Users must submit a first name"

def test_create_user_with_no_lastname(user_factory):
    """Test create user with no last name"""
    with pytest.raises(ValueError) as err:
        user_factory.create(last_name=None)
    assert str(err.value) == "Users must submit a last name"

def test_create_superuser_with_no_email(user_factory):
    """Test create super user with no email"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=True, email=None)
    assert str(err.value) == "Admin Account: An email address is required"

def test_create_superuser_with_no_password(user_factory):
    """Test create super user with no password"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=True, password=None)
    assert str(err.value) == "Superusers must have a password"

def test_create_user_with_invalid_email(user_factory):
    """Test create user with invalid email"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email="test@example")
    assert str(err.value) == "You must provide a valid email address"
