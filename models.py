"""Data models for the FlavorHub Recipe Manager application."""


class Recipe:
    """Represents a recipe with dietary tags and metadata."""

    def __init__(self, recipe_id, name, cuisine, dietary_tags=None, ingredients=None):
        self.recipe_id = recipe_id
        self.name = name
        self.cuisine = cuisine
        self.dietary_tags = dietary_tags if dietary_tags is not None else []
        self.ingredients = ingredients if ingredients is not None else []

    def __repr__(self):
        return f"Recipe(id={self.recipe_id!r}, name={self.name!r}, cuisine={self.cuisine!r})"


class User:
    """Represents an application user with optional dietary restrictions."""

    def __init__(self, user_id, name, dietary_restrictions=None):
        self.user_id = user_id
        self.name = name
        # Default to empty list so iteration is always safe
        self.dietary_restrictions = dietary_restrictions if dietary_restrictions is not None else []

    def __repr__(self):
        return f"User(id={self.user_id!r}, name={self.name!r})"


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_RECIPES = [
    Recipe("r1", "Spaghetti Carbonara", "Italian", ["gluten-free-friendly"], ["pasta", "eggs", "pancetta"]),
    Recipe("r2", "Margherita Pizza", "Italian", [], ["dough", "tomato", "mozzarella"]),
    Recipe("r3", "Grilled Salmon", "Mediterranean", ["gluten-free", "dairy-free"], ["salmon", "lemon", "herbs"]),
    Recipe("r4", "Vegan Buddha Bowl", "Asian", ["vegan", "gluten-free", "dairy-free"], ["quinoa", "tofu", "vegetables"]),
    Recipe("r5", "Beef Tacos", "Mexican", ["gluten-free"], ["beef", "tortilla", "salsa"]),
    Recipe("r6", "Mushroom Risotto", "Italian", ["vegetarian", "gluten-free"], ["arborio rice", "mushrooms", "parmesan"]),
]

SAMPLE_USERS = [
    User("u1", "Alice", dietary_restrictions=["vegan", "gluten-free"]),
    # Bob has no dietary restrictions — dietary_restrictions defaults to []
    User("u2", "Bob"),
    User("u3", "Carol", dietary_restrictions=["dairy-free"]),
]
