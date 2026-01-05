from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from categories.models import Category
from recipes.forms import AddRecipeForm, RecipeSearchForm
from recipes.models import Recipe


class RecipeModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Dinner", description="Evening meals")
        self.recipe = Recipe.objects.create(
            name="Tomato Pasta",
            description="Simple pasta recipe.",
            ingredients="pasta,tomato,garlic",
            cooking_time=15,
            difficulty="",
            category=self.category,
        )

    def test_str_returns_name(self):
        self.assertEqual(str(self.recipe), "Tomato Pasta")

    def test_get_absolute_url(self):
        url = self.recipe.get_absolute_url()
        expected = reverse("recipes:recipe_detail", kwargs={"pk": self.recipe.pk})
        self.assertEqual(url, expected)

    def test_calculate_difficulty_easy(self):
        recipe = Recipe.objects.create(
            name="Toast",
            description="Toast it.",
            ingredients="bread,butter",
            cooking_time=5,
            difficulty="",
        )
        self.assertEqual(recipe.calculate_difficulty(), "Easy")

    def test_calculate_difficulty_medium(self):
        recipe = Recipe.objects.create(
            name="Omelette",
            description="Eggs and stuff.",
            ingredients="eggs,milk,salt,pepper",
            cooking_time=12,
            difficulty="",
        )
        self.assertEqual(recipe.calculate_difficulty(), "Medium")

    def test_calculate_difficulty_hard(self):
        recipe = Recipe.objects.create(
            name="Curry",
            description="Spicy.",
            ingredients="onion,garlic,ginger,spices,tomato,chicken,rice",
            cooking_time=25,
            difficulty="",
        )
        self.assertEqual(recipe.calculate_difficulty(), "Hard")

    def test_calculate_difficulty_very_hard(self):
        recipe = Recipe.objects.create(
            name="Big Feast",
            description="Complex.",
            ingredients="a,b,c,d,e,f,g,h,i,j,k",
            cooking_time=45,
            difficulty="",
        )
        self.assertEqual(recipe.calculate_difficulty(), "Very Hard")

    def test_recipe_can_have_category_null(self):
        recipe = Recipe.objects.create(
            name="No Category Dish",
            description="Test.",
            ingredients="a,b",
            cooking_time=10,
            difficulty="",
            category=None,
        )
        self.assertIsNone(recipe.category)


class RecipeFormTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Dessert", description="")

    def test_recipe_search_form_valid_empty(self):
        """
        Search form should be valid even if empty (all fields optional).
        """
        form = RecipeSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_recipe_search_form_invalid_negative_time(self):
        form = RecipeSearchForm(data={"max_cooking_time": -5})
        self.assertFalse(form.is_valid())
        self.assertIn("max_cooking_time", form.errors)

    def test_add_recipe_form_valid_minimal(self):
        """
        Recipe model requires: name, description, ingredients, cooking_time.
        Pic has a default so we can omit it.
        Category can be blank.
        """
        form_data = {
            "name": "Apple Pie",
            "description": "Bake it.",
            "ingredients": "apple,flour,sugar",
            "cooking_time": 30,
            "category": self.category.pk,
        }
        form = AddRecipeForm(data=form_data, files={})
        self.assertTrue(form.is_valid(), form.errors)

        recipe = form.save()
        self.assertEqual(recipe.name, "Apple Pie")
        self.assertEqual(recipe.category, self.category)

    def test_add_recipe_form_invalid_missing_required_fields(self):
        form = AddRecipeForm(data={"name": "Only Name"})
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)
        self.assertIn("ingredients", form.errors)
        self.assertIn("cooking_time", form.errors)


class RecipeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.category = Category.objects.create(name="Lunch", description="")
        self.recipe = Recipe.objects.create(
            name="Salad",
            description="Mix ingredients.",
            ingredients="lettuce,tomato,cucumber",
            cooking_time=8,
            difficulty="",
            category=self.category,
        )

    def test_home_page_public(self):
        url = reverse("recipes:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipes_home.html")

    def test_recipes_overview_requires_login(self):
        url = reverse("recipes:recipes_overview")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_recipe_detail_requires_login(self):
        url = reverse("recipes:recipe_detail", kwargs={"pk": self.recipe.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_recipe_search_requires_login(self):
        url = reverse("recipes:recipe_search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_recipe_add_requires_login(self):
        url = reverse("recipes:recipe_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_logged_in_can_view_overview(self):
        self.client.login(username="testuser", password="testpass123")
        url = reverse("recipes:recipes_overview")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipes_overview.html")
        self.assertContains(response, "Salad")

    def test_logged_in_can_view_detail(self):
        self.client.login(username="testuser", password="testpass123")
        url = reverse("recipes:recipe_detail", kwargs={"pk": self.recipe.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_detail.html")
        self.assertContains(response, "Salad")

    def test_logged_in_can_open_add_recipe_form(self):
        self.client.login(username="testuser", password="testpass123")
        url = reverse("recipes:recipe_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_add.html")

    def test_logged_in_can_post_add_recipe_without_image(self):
        """
        Pic has a default (no_picture.jpg), so omitting FILES should still work.
        """
        self.client.login(username="testuser", password="testpass123")
        url = reverse("recipes:recipe_add")

        post_data = {
            "name": "New Dish",
            "description": "Steps here.",
            "ingredients": "a,b,c",
            "cooking_time": 12,
            "category": self.category.pk,
        }

        response = self.client.post(url, data=post_data, follow=False)
        self.assertEqual(response.status_code, 302)

        created = Recipe.objects.get(name="New Dish")
        expected_detail = reverse("recipes:recipe_detail", kwargs={"pk": created.pk})
        self.assertEqual(response["Location"], expected_detail)

    def test_logged_in_search_post_returns_results_count(self):
        """
        Basic smoke test: POST search should respond 200 and show result count.
        We avoid asserting chart output (matplotlib) to keep tests stable.
        """
        self.client.login(username="testuser", password="testpass123")
        url = reverse("recipes:recipe_search")

        response = self.client.post(
            url,
            data={
                "recipe_name": "Sal",
                "ingredient": "",
                "max_cooking_time": "",
                "chart_type": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_search.html")
        self.assertContains(response, "Results:")
