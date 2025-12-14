from django.db import models
from django.urls import reverse


class Recipe(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    ingredients = models.TextField(
        help_text="Comma-separated list of ingredients"
    )
    cooking_time = models.PositiveIntegerField(
        help_text="Cooking time in minutes"
    )
    difficulty = models.CharField(max_length=20, blank=True)

    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipes'
    )

    pic = models.ImageField(
        upload_to='recipes',
        default='no_picture.jpg'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'pk': self.pk})

    def calculate_difficulty(self):
    
        ingredients_list = [i.strip() for i in self.ingredients.split(',') if i.strip()]
        num_ingredients = len(ingredients_list)

        if self.cooking_time < 10 and num_ingredients < 4:
            return "Easy"
        elif self.cooking_time < 20 and num_ingredients <= 6:
            return "Medium"
        elif self.cooking_time < 30 and num_ingredients <= 10:
            return "Hard"
        else:
            return "Very Hard"
