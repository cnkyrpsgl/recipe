from django.urls import path, include
from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('<int:recipe_id>', views.detail, name='detail'),
    path('<int:recipe_id>/upvote', views.upvote, name='upvote'),
    path('<int:recipe_id>/rate', views.rate, name='rate'),
    path('myrecipes/', views.myrecipes, name = 'myrecipes'),
    path('iglist', views.iglist, name='iglist'),
    path('recipes/<int:ingredient_id>', views.recipes, name = 'recipes'),
    path('<int:recipe_id>/delete', views.delete, name = 'delete'),
    path('<int:recipe_id>/edit', views.edit, name = 'edit'),
]
