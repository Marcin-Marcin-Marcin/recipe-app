
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .forms import RecipeSearchForm
from .models import Recipe


User = get_user_model()


class RecipeSearchFormTest(TestCase):
    def test_form_has_expected_fields(self):
        form = RecipeSearchForm()
        self.assertIn("recipe_name", form.fields)
        self.assertIn("ingredient", form.fields)
        self.assertIn("max_cooking_time", form.fields)
        self.assertIn("chart_type", form.fields)

    def test_form_valid_with_empty_data(self):
        form = RecipeSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_max_cooking_time_must_be_positive(self):
        form = RecipeSearchForm(data={"max_cooking_time": 0})
        self.assertFalse(form.is_valid())
        self.assertIn("max_cooking_time", form.errors)

    def test_chart_choices_include_no_chart(self):
        form = RecipeSearchForm()
        choices = [c[0] for c in form.fields["chart_type"].choices]
        self.assertIn("", choices)   
        self.assertIn("#1", choices)
        self.assertIn("#2", choices)
        self.assertIn("#3", choices)


class RecipeAuthAndViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass123")

        cls.r1 = Recipe.objects.create(
            name="Pasta Primavera",
            description="Pasta with vegetables",
            ingredients="pasta, garlic, tomato",
            cooking_time=15,
            difficulty="Medium",
        )
        cls.r2 = Recipe.objects.create(
            name="Tomato Soup",
            description="Simple soup",
            ingredients="tomato, onion, garlic",
            cooking_time=25,
            difficulty="Easy",
        )
        cls.r3 = Recipe.objects.create(
            name="Chocolate Cake",
            description="Dessert",
            ingredients="flour, sugar, milk, cocoa",
            cooking_time=45,
            difficulty="Hard",
        )


    def test_recipes_overview_requires_login(self):
        url = reverse("recipes:recipes_overview")  
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/?next=", resp.url)
        self.assertIn(url, resp.url)

    def test_recipe_detail_requires_login(self):
        url = reverse("recipes:recipe_detail", args=[self.r1.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/?next=", resp.url)
        self.assertIn(url, resp.url)

    def test_recipe_search_requires_login(self):
        url = reverse("recipes:recipe_search")  
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/?next=", resp.url)
        self.assertIn(url, resp.url)


    def login(self):
        self.client.login(username="testuser", password="testpass123")

    def test_search_get_shows_all_recipes(self):
        self.login()
        url = reverse("recipes:recipe_search")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        self.assertIn("results_count", resp.context)
        self.assertEqual(resp.context["results_count"], Recipe.objects.count())


        html = resp.content.decode("utf-8")
        self.assertIn('class="dataframe recipe-search-table"', html)
        self.assertIn(reverse("recipes:recipe_detail", args=[self.r1.pk]), html)
        self.assertIn('class="recipe-link"', html)

    def test_search_partial_name_match(self):
        self.login()
        url = reverse("recipes:recipe_search")

        resp = self.client.post(url, data={"recipe_name": "pasta"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["results_count"], 1)

        html = resp.content.decode("utf-8").lower()
        self.assertIn("pasta primavera".lower(), html)
        self.assertNotIn("tomato soup".lower(), html)

    def test_search_ingredient_match(self):
        self.login()
        url = reverse("recipes:recipe_search")

        resp = self.client.post(url, data={"ingredient": "garlic"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["results_count"], 2)

        html = resp.content.decode("utf-8").lower()
        self.assertIn("pasta primavera".lower(), html)
        self.assertIn("tomato soup".lower(), html)
        self.assertNotIn("chocolate cake".lower(), html)

    def test_search_max_cooking_time_filter(self):
        self.login()
        url = reverse("recipes:recipe_search")

        resp = self.client.post(url, data={"max_cooking_time": 20})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["results_count"], 1)

        html = resp.content.decode("utf-8").lower()
        self.assertIn("pasta primavera".lower(), html)
        self.assertNotIn("tomato soup".lower(), html)
        self.assertNotIn("chocolate cake".lower(), html)

    def test_search_combined_filters(self):
        self.login()
        url = reverse("recipes:recipe_search")

        resp = self.client.post(url, data={"recipe_name": "tomato", "ingredient": "garlic"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["results_count"], 1)

        html = resp.content.decode("utf-8").lower()
        self.assertIn("tomato soup".lower(), html)
        self.assertNotIn("pasta primavera".lower(), html)


    def test_chart_not_rendered_if_no_chart_selected(self):
        self.login()
        url = reverse("recipes:recipe_search")

        resp = self.client.post(url, data={"recipe_name": "tomato", "chart_type": ""})
        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(resp.context.get("chart"))

        html = resp.content.decode("utf-8")
        self.assertNotIn("data:image/png;base64", html)

    def test_chart_renders_when_chart_type_selected(self):
        self.login()
        url = reverse("recipes:recipe_search")

        resp = self.client.post(url, data={"ingredient": "garlic", "chart_type": "#1"})
        self.assertEqual(resp.status_code, 200)

        chart = resp.context.get("chart")
        self.assertIsNotNone(chart)
        self.assertTrue(isinstance(chart, str))
        self.assertGreater(len(chart), 50)  

        html = resp.content.decode("utf-8")
        self.assertIn("data:image/png;base64", html)


    def test_calculate_difficulty_returns_expected_value(self):
        self.assertEqual(self.r1.calculate_difficulty(), "Medium")
