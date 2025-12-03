from django.test import TestCase
from .models import Category


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(
            name="Dessert",
            description="Sweet dishes"
        )

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_str_returns_name(self):
        category = Category.objects.get(id=1)
        self.assertEqual(str(category), "Dessert")
