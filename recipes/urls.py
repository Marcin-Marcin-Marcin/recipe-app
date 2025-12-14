from django.urls import path
from .views import recipes_home, RecipeListView, RecipeDetailView

app_name = 'recipes'

urlpatterns = [
    # homepage
    path('', recipes_home, name='home'),

    # all recipes
    path('recipes/', RecipeListView.as_view(), name='recipes_overview'),

    # a single recipe
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
]
