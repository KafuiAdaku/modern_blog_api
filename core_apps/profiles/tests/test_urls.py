import pytest
from django.urls import reverse, resolve


def test_all_profiles():
    """Test all profiles url"""
    path = reverse("profiles:all_profiles")
    assert resolve(path).view_name == "profiles:all_profiles"
