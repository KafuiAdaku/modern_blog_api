import pytest
from core_apps.profiles.models import Profile

def test_profile_str(profile):
    """Test profile string representation"""
    assert profile.__str__ == f"{profile.user.username}'profile"
