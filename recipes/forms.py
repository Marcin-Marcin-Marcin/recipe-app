from django import forms

CHART_CHOICES = (
    ("", "— No chart —"),
    ("#1", "Bar chart (cooking time per recipe)"),
    ("#2", "Pie chart (difficulty distribution)"),
    ("#3", "Line chart (cooking time trend)"),
)


class RecipeSearchForm(forms.Form):
    recipe_name = forms.CharField(
        required=False,
        max_length=120,
        label="Recipe name contains",
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g. pasta, soup, cake",
                "class": "form-control",
                "autocomplete": "off",
            }
        ),
    )

    ingredient = forms.CharField(
        required=False,
        max_length=120,
        label="Ingredient contains",
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g. garlic, milk",
                "class": "form-control",
                "autocomplete": "off",
            }
        ),
    )

    max_cooking_time = forms.IntegerField(
        required=False,
        min_value=1,
        label="Max cooking time (minutes)",
        widget=forms.NumberInput(
            attrs={
                "placeholder": "e.g. 30",
                "class": "form-control",
                "min": 1,
                "step": 1,
            }
        ),
    )

    chart_type = forms.ChoiceField(
        required=False,
        choices=CHART_CHOICES,
        label="Chart type (optional)",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )
