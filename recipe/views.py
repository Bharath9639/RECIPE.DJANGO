from django.shortcuts import render, redirect
from recipe.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url= "/login")
def recipe(request):
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_img =request.FILES.get('recipe_img')  

        Recipe.objects.create(
            recipe_name = recipe_name,
            recipe_description = recipe_description,
            recipe_img = recipe_img
        ) 
        return redirect("/recipe")
    recipes = Recipe.objects.all()

    if request.GET.get('Search'):
        recipes = recipes.filter(recipe_name__icontains = request.GET.get('Search'))


    return render(request , 'index.html', context={"recipes" : recipes})

@login_required(login_url= "/login")
def delete_recipe(request ,  id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect("/recipe")

@login_required(login_url= "/login")
def update_recipe(request , id):
   queryset = Recipe.objects.get(id=id)
   if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_img =request.FILES.get('recipe_img') 


        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description
        queryset.recipe_img = recipe_img

        queryset.save()
        return redirect("/recipe") 


   return render(request , "update-recipe.html" , context = {"recipe" : queryset})


def registration(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')


        if User.objects.filter(username = username).exists():
            messages.error(request, "username already exists, try different username")
            return redirect("/registration")

        user =  User.objects.create(first_name = first_name , last_name = last_name , username = username )
        user.set_password(password)
        user.save()

        messages.success(request, "Account is created Successfully")

       
        
        return redirect("/login")
        
    return render(request, "registration.html")

def login_page(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, "Invalid username")
            return redirect("/login")
        
        user = authenticate(username = username , password = password)
        if user is None:
            messages.error(request , "Invalid credentials")
            return redirect("/login")
        
        else:
            login(request , user)
            return redirect("/recipe")


    return render(request , "login.html")

def logout_page(request):
    logout(request)
    return redirect("/login")
