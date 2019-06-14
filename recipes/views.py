from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Recipe, RecipeForm, Rate, Ingredient
from django.utils import timezone
from django.core.paginator import Paginator

def home(request):
    recipes = Recipe.objects.order_by('-pub_date')
    per_page = 5
    paginator = Paginator(recipes, per_page)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    ingredients = Ingredient.objects.order_by('-recipe_total')[:5]
    return render(request, 'recipes/home.html', {'recipes': recipes, 'ingredients': ingredients})

@login_required(login_url='/accounts/signup')
def myrecipes(request):
    recipes = Recipe.objects.filter(author=request.user).order_by('-pub_date')
    return render(request, 'recipes/myrecipes.html', {'recipes':recipes})

def recipes(request, ingredient_id):
    recipes = Recipe.objects.filter(ingredient=ingredient_id).order_by('-pub_date')
    return render(request, 'recipes/myrecipes.html', {'recipes':recipes})

def iglist(request):
    if request.method == 'POST':
        ig_name = request.POST["ig_name"]
        try:
            id = Ingredient.objects.get(name=ig_name).id
            return recipes(request, id)
        except:
            return home(request)


@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['description'] and request.FILES['image']:
            recipe = Recipe()
            recipe.title = request.POST['title']
            recipe.description = request.POST['description']
            recipe.image = request.FILES['image']
            recipe.pub_date = timezone.now()
            recipe.author = request.user
            recipe.difficulty = request.POST["difficulty"]
            recipe.save()
            for ingredient in request.POST.getlist('ingredients'):
                try:
                    ig = Ingredient.objects.get(name=ingredient)
                except:
                    ig = Ingredient(name=ingredient)
                ig.save()
                if recipe not in ig.recipes.all():
                    ig.recipes.add(recipe)
                    ig.recipe_total += 1
                ig.save()
            return redirect('/recipes/' + str(recipe.id))
        else:
            return render(request, 'recipes/create.html',{'error':'All fields are required.'})
    else:
        rform = RecipeForm()
        return render(request, 'recipes/create.html', { 'RecipeForm': rform})

@login_required(login_url='/accounts/signup')
def edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    rform = RecipeForm(instance=recipe)
    if request.method == 'POST':
        if request.POST['title'] and request.POST['description'] and request.FILES['image']:
            recipe.title = request.POST['title']
            recipe.description = request.POST['description']
            recipe.image = request.FILES['image']
            recipe.pub_date = timezone.datetime.now()
            recipe.author = request.user
            recipe.difficulty = request.POST["difficulty"]
            recipe.save()
            return redirect('/recipes/' + str(recipe.id))
        else:
            return render(request, 'recipes/edit.html',{'error':'All fields are required.', 'RecipeForm': rform})
    else:
        return render(request, 'recipes/edit.html', { 'RecipeForm': rform})

def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    igs = Ingredient.objects.filter(recipes=recipe)
    return render(request, 'recipes/detail.html', {'recipe': recipe, 'igs': igs})


@login_required(login_url='/accounts/signup')
def delete(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.delete()
        return myrecipes(request)

@login_required(login_url="/accounts/signup")
def upvote(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.user in recipe.likes.all():
            recipe.likes.remove(request.user)
            recipe.likes_total -= 1
        else:
            recipe.likes.add(request.user)
            recipe.likes_total += 1
        recipe.save()
        return redirect('/recipes/' + str(recipe.id))

@login_required(login_url="/accounts/signup")
def rate(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        try:
            rt = Rate.objects.get(rater=request.user, rated=recipe)
            recipe.rate_avg = (recipe.rate_avg * recipe.rate_total - rt.value + int(request.POST['rate_val'])) / recipe.rate_total
        except:
            rt = Rate(rater=request.user, rated=recipe, value=int(request.POST['rate_val']))
            rt.save()
            recipe.rate_avg = (recipe.rate_avg * recipe.rate_total + int(request.POST['rate_val'])) / (recipe.rate_total + 1)
            recipe.rate_total += 1
        recipe.save()
        return redirect('/recipes/' + str(recipe.id))
