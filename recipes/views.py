from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Recipe
from .forms import RecipeSearchForm
from .utils import get_chart


def recipes_home(request):
    """
    Simple homepage view for the Recipe app.
    """
    return render(request, "recipes/recipes_home.html")


class RecipeListView(LoginRequiredMixin, ListView):
    """
    Shows a list of all recipes (protected).
    """
    model = Recipe
    template_name = "recipes/recipes_overview.html"


class RecipeDetailView(LoginRequiredMixin, DetailView):
    """
    Shows the details of a single recipe (protected).
    """
    model = Recipe
    template_name = "recipes/recipe_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ingredients_raw = self.object.ingredients or ""
        ingredients_list = [i.strip() for i in ingredients_raw.split(",") if i.strip()]

        context["ingredients_list"] = ingredients_list
        context["difficulty"] = self.object.calculate_difficulty()
        return context


@login_required
def recipe_search(request):
    """
    Protected search page:
    - Reads input from RecipeSearchForm
    - Filters recipes using QuerySet API
    - Converts results into a pandas DataFrame
    - Displays results as an HTML table (clickable names)
    - OPTIONAL charts (bar/pie/line) based on chart_type
    """
    import pandas as pd

    form = RecipeSearchForm(request.POST or None)

    qs = Recipe.objects.all().order_by("name")

    results_df_html = None
    chart = None

    if request.method == "POST" and form.is_valid():
        recipe_name = (form.cleaned_data.get("recipe_name") or "").strip()
        ingredient = (form.cleaned_data.get("ingredient") or "").strip()
        max_time = form.cleaned_data.get("max_cooking_time")
        chart_type = form.cleaned_data.get("chart_type") 

        if recipe_name:
            qs = qs.filter(name__icontains=recipe_name)

        if ingredient:
            qs = qs.filter(ingredients__icontains=ingredient)

        if max_time:
            qs = qs.filter(cooking_time__lte=max_time)

    if qs.exists():
        df = pd.DataFrame(list(qs.values("id", "name", "cooking_time", "difficulty", "ingredients")))

        chart_type = None
        if request.method == "POST" and form.is_valid():
            chart_type = form.cleaned_data.get("chart_type")

        df_chart = df[["name", "cooking_time", "difficulty"]].copy()
        chart = get_chart(chart_type, df_chart)

        df["name"] = df.apply(
            lambda row: f'<a class="recipe-link" href="{reverse("recipes:recipe_detail", args=[row["id"]])}">{row["name"]}</a>',
            axis=1,
        )

        df["ingredients"] = df["ingredients"].fillna("").apply(
            lambda x: x if len(x) <= 80 else x[:77] + "..."
        )

        df = df.drop(columns=["id"])

        results_df_html = df.to_html(
            classes="recipe-search-table",
            index=False,
            escape=False,
        )

    context = {
        "form": form,
        "results_df": results_df_html,
        "results_count": qs.count(),
        "chart": chart,
    }
    return render(request, "recipes/recipe_search.html", context)
