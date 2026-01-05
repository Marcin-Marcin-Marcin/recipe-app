from django.test import TestCase
from categories.models import Category


class CategoryModelTests(TestCase):
    def test_str_returns_name(self):
        category = Category.objects.create(name="Dessert", description="Sweet things")
        self.assertEqual(str(category), "Dessert")

    def test_description_can_be_blank(self):
        category = Category.objects.create(name="Breakfast", description="")
        self.assertEqual(category.description, "")
