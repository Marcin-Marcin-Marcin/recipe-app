from django.urls import path
from .views import recipes_home, RecipeListView, RecipeDetailView, recipe_search, recipe_add

app_name = "recipes"

urlpatterns = [
    path("", recipes_home, name="home"),
    path("recipes/", RecipeListView.as_view(), name="recipes_overview"),
    path("recipes/<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("search/", recipe_search, name="recipe_search"),

    # add recipe (logged-in users)
    path("recipes/add/", recipe_add, name="recipe_add"),
]
