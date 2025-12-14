from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe


def recipes_home(request):
    """
    Simple homepage view for the Recipe app.
    """
    return render(request, 'recipes/recipes_home.html')


class RecipeListView(ListView):
    """
    Shows a list of all recipes.
    """
    model = Recipe
    template_name = 'recipes/recipes_overview.html'


class RecipeDetailView(DetailView):
    """
    Shows the details of a single recipe.
    """
    model = Recipe
    template_name = 'recipes/recipe_detail.html'

    def get_context_data(self, **kwargs):
        """
        Add extra data for the template:
        - ingredients_list: list of ingredients
        - difficulty: value from calculate_difficulty()
        """
        context = super().get_context_data(**kwargs)

        ingredients_raw = self.object.ingredients or ""
        ingredients_list = [
            i.strip() for i in ingredients_raw.split(",") if i.strip()
        ]

        context["ingredients_list"] = ingredients_list
        context["difficulty"] = self.object.calculate_difficulty()

        return context
