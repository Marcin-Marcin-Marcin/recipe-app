
from django.test import TestCase
from django.urls import reverse
from .models import Recipe


class RecipeModelTest(TestCase):
    """
    Basic tests for the Recipe model fields and __str__ method.
    """

    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(
            name="Test Recipe",
            description="A simple test recipe",
            ingredients="onion, garlic, tomato",
            cooking_time=20,
            difficulty="Easy"
        )

    def test_name_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 120)

    def test_str_returns_name(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(recipe), "Test Recipe")


class RecipeViewTests(TestCase):
    """
    Tests for recipe views and URL behaviour.
    """

    @classmethod
    def setUpTestData(cls):
        cls.recipe = Recipe.objects.create(
            name="View Test Recipe",
            description="Description for view tests",
            ingredients="egg, milk",
            cooking_time=5,
            difficulty="Easy"
        )

    def test_get_absolute_url(self):
        """
        get_absolute_url should return /recipes/<pk>/ for a recipe.
        """
        expected_url = f"/recipes/{self.recipe.pk}/"
        self.assertEqual(self.recipe.get_absolute_url(), expected_url)

    def test_recipes_overview_status_code(self):
        """
        /recipes/ (named 'recipes_overview') should return HTTP 200.
        """
        url = reverse('recipes:recipes_overview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_status_code(self):
        """
        /recipes/<pk>/ (named 'recipe_detail') should return HTTP 200
        for an existing recipe.
        """
        url = reverse('recipes:recipe_detail', args=[self.recipe.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
