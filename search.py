"""Search functionality for the FlavorHub Recipe Manager application."""

from models import SAMPLE_RECIPES


def filter_by_cuisine(recipes, cuisine):
    """Return recipes that match the given cuisine (case-insensitive).

    If *cuisine* is falsy the original list is returned unchanged.
    """
    if not cuisine:
        return recipes
    cuisine_lower = cuisine.lower()
    return [r for r in recipes if r.cuisine.lower() == cuisine_lower]


def filter_by_ingredient(recipes, ingredient):
    """Return recipes that contain *ingredient* (case-insensitive).

    If *ingredient* is falsy the original list is returned unchanged.
    """
    if not ingredient:
        return recipes
    ingredient_lower = ingredient.lower()
    return [r for r in recipes if any(ingredient_lower in i.lower() for i in r.ingredients)]


def filter_by_dietary(recipes, user):
    """Return only recipes that satisfy all of the user's dietary restrictions.

    If the user has no dietary restrictions (``None`` or empty list) every
    recipe passes through unchanged — no filtering is applied.

    Args:
        recipes: iterable of :class:`~models.Recipe` objects.
        user: a :class:`~models.User` instance whose ``dietary_restrictions``
              attribute may be ``None`` or an empty list.

    Returns:
        A list of :class:`~models.Recipe` objects that match the user's
        dietary requirements.
    """
    # Guard: skip dietary filtering when the user has no restrictions
    if not user.dietary_restrictions:
        return list(recipes)

    result = list(recipes)
    for restriction in user.dietary_restrictions:
        result = [r for r in result if restriction in r.dietary_tags]
    return result


def search_recipes(query=None, cuisine=None, ingredient=None, user=None, recipes=None):
    """Search recipes by keyword, cuisine, ingredient and/or dietary needs.

    Args:
        query: optional keyword to match against recipe names
               (case-insensitive substring match).
        cuisine: optional cuisine name to filter by.
        ingredient: optional ingredient name to filter by.
        user: optional :class:`~models.User` whose dietary restrictions are
              applied as a filter.  When ``None`` no dietary filter is applied.
        recipes: the recipe collection to search; defaults to
                 :data:`~models.SAMPLE_RECIPES`.

    Returns:
        A list of matching :class:`~models.Recipe` objects.
    """
    if recipes is None:
        recipes = SAMPLE_RECIPES

    results = list(recipes)

    if query:
        query_lower = query.lower()
        results = [r for r in results if query_lower in r.name.lower()]

    if cuisine:
        results = filter_by_cuisine(results, cuisine)

    if ingredient:
        results = filter_by_ingredient(results, ingredient)

    if user is not None:
        results = filter_by_dietary(results, user)

    return results
