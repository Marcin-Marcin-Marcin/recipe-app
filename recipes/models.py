from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    ingredients = models.TextField(help_text="Comma-separated list of ingredients")
    cooking_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    difficulty = models.CharField(max_length=20)
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipes'
    )

    def __str__(self):
        return self.name
