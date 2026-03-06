"""Tests for the search module — specifically the dietary restriction bug fix."""

import sys
import os

# Ensure the project root is on sys.path so imports work when running pytest
# from any directory.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from models import Recipe, User, SAMPLE_USERS
from search import filter_by_dietary, search_recipes


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_recipes():
    return [
        Recipe("r1", "Vegan Salad", "American", ["vegan", "gluten-free", "dairy-free"]),
        Recipe("r2", "Cheese Pizza", "Italian", ["vegetarian"]),
        Recipe("r3", "Grilled Chicken", "American", ["gluten-free", "dairy-free"]),
        Recipe("r4", "Pasta Primavera", "Italian", ["vegetarian", "dairy-free"]),
    ]


# ---------------------------------------------------------------------------
# Bug fix: filter_by_dietary with None / empty dietary_restrictions
# ---------------------------------------------------------------------------

class TestFilterByDietaryNullGuard:
    """Regression tests for the TypeError when dietary_restrictions is None."""

    def test_user_with_none_dietary_restrictions_does_not_crash(self, sample_recipes):
        """filter_by_dietary must not raise TypeError when dietary_restrictions is None."""
        user = User("u99", "NoDietUser", dietary_restrictions=None)
        # Should not raise — previously crashed with TypeError
        result = filter_by_dietary(sample_recipes, user)
        assert result == sample_recipes

    def test_user_with_empty_list_returns_all_recipes(self, sample_recipes):
        """An empty dietary_restrictions list must return all recipes unchanged."""
        user = User("u99", "NoDietUser", dietary_restrictions=[])
        result = filter_by_dietary(sample_recipes, user)
        assert result == sample_recipes

    def test_bob_from_sample_users_does_not_crash(self, sample_recipes):
        """Bob (no dietary restrictions) must not cause a crash — production scenario."""
        bob = next(u for u in SAMPLE_USERS if u.name == "Bob")
        # This call previously raised TypeError in production
        result = filter_by_dietary(sample_recipes, bob)
        assert result == sample_recipes

    def test_bob_search_does_not_crash(self, sample_recipes):
        """search_recipes with Bob (no dietary restrictions) must not crash."""
        bob = next(u for u in SAMPLE_USERS if u.name == "Bob")
        result = search_recipes(user=bob, recipes=sample_recipes)
        assert result == sample_recipes

    def test_search_pasta_italian_for_bob(self):
        """Full search for 'pasta' / Italian cuisine for Bob must return results."""
        bob = next(u for u in SAMPLE_USERS if u.name == "Bob")
        # Regression: this call crashed 500 Internal Server Error in production
        result = search_recipes(query="pasta", cuisine="Italian", user=bob)
        assert isinstance(result, list)
        # Every returned recipe should be Italian and contain 'pasta' in name
        for r in result:
            assert r.cuisine.lower() == "italian"
            assert "pasta" in r.name.lower()


# ---------------------------------------------------------------------------
# Correct filtering when restrictions are present
# ---------------------------------------------------------------------------

class TestFilterByDietaryWithRestrictions:
    """Verify that dietary filtering still works correctly when restrictions exist."""

    def test_vegan_filter(self, sample_recipes):
        user = User("u1", "Alice", dietary_restrictions=["vegan"])
        result = filter_by_dietary(sample_recipes, user)
        assert all("vegan" in r.dietary_tags for r in result)

    def test_multiple_restrictions(self, sample_recipes):
        user = User("u1", "Alice", dietary_restrictions=["gluten-free", "dairy-free"])
        result = filter_by_dietary(sample_recipes, user)
        for r in result:
            assert "gluten-free" in r.dietary_tags
            assert "dairy-free" in r.dietary_tags

    def test_no_matching_recipes_returns_empty(self, sample_recipes):
        user = User("u1", "Alice", dietary_restrictions=["kosher"])
        result = filter_by_dietary(sample_recipes, user)
        assert result == []


# ---------------------------------------------------------------------------
# User model default
# ---------------------------------------------------------------------------

class TestUserModelDefault:
    """Verify that User.dietary_restrictions defaults to [] (not None)."""

    def test_default_dietary_restrictions_is_empty_list(self):
        user = User("u0", "Test")
        assert user.dietary_restrictions == []
        assert user.dietary_restrictions is not None

    def test_explicit_none_becomes_empty_list(self):
        user = User("u0", "Test", dietary_restrictions=None)
        assert user.dietary_restrictions == []

    def test_explicit_list_is_preserved(self):
        restrictions = ["vegan", "gluten-free"]
        user = User("u0", "Test", dietary_restrictions=restrictions)
        assert user.dietary_restrictions == restrictions
