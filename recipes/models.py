from django.db import models
from django.forms import ModelForm, MultipleChoiceField, CheckboxSelectMultiple
from django.contrib.auth.models import User

DIFFICULTY_CHOICES = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
)

RATE_MAX = 5
RATE_CHOICES = (
    (x, x) for x in range(RATE_MAX + 1)
)

INGREDIENT_CHOICES = (
    ('tomato', 'Tomato'),
    ('eggplant', 'Eggplant'),
    ('celery', 'Celery'),
    ('egg', 'Egg'),
    ('milk', 'Milk'),
    ('fish', 'Fish'),
    ('chicken', 'Chicken'),
    ('oil', 'Oil'),
)


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    likes_total = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='likers')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES, default='easy')
    rate_val = models.IntegerField(choices=RATE_CHOICES, default=RATE_MAX)
    rate_max = RATE_MAX
    rate_avg = models.FloatField(default=0)
    rate_total = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def summary(self):
        return self.description[:100]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%x')


class Rate(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE)
    rated = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    value = models.IntegerField(default=0, choices=RATE_CHOICES)


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    recipe_total = models.IntegerField(default=0)
    recipes = models.ManyToManyField(Recipe)


class RecipeForm(ModelForm):
    ingredients = MultipleChoiceField(choices=INGREDIENT_CHOICES,widget=CheckboxSelectMultiple)
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'description', 'difficulty']
