from datetime import datetime
from django.shortcuts import render
from django.views import View 
from django.core.paginator import Paginator
from django.shortcuts import render, render_to_response,redirect,get_object_or_404
from random import randint, shuffle
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from jedzonko.models import Recipe, Plan, DayName, RecipePlan
from django.core.exceptions import ObjectDoesNotExist



class IndexView(View):
    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)

class About(View):

    def get(self, request):  
        return render(request,"about.html")

class Contact(View): 

    def get(self, request):
        return render(request,"contact.html")

class Main(View): 

    def get(self, request):
        return render(request,"index.html")

class LandingPage(View):
    def get(self, request):
        recipes_number = Recipe.objects.all().count()
        numbers = list(range(1, int(recipes_number)))
        shuffle(numbers)
        random1 = numbers.pop()
        random2 = numbers.pop()
        random3 = numbers.pop()

        recipes = Recipe.objects.filter(pk=random1) | Recipe.objects.filter(pk=random2) | Recipe.objects.filter(pk=random3)

        ctx = {"recipes": recipes}
        return render(request, "index.html", ctx)


class RecipesList(View):

    def get(self,request):

        recipes = Recipe.objects.order_by("-votes", "-created")
        paginator = Paginator(recipes,3)

        page = request.GET.get('page')
        sorted = paginator.get_page(page)

        ctx = {"recipes": sorted}
        return render(request, 'recipes.html', ctx)


class MainPage(View):
    def get(self,request):
        plans_number = Plan.objects.all().count()
        recipes_number = Recipe.objects.all().count()

        get_plans = Plan.objects.order_by("created")
        get_first_plan=get_plans[0]
        day_name= DayName.objects.all().order_by("order")
        plan_recipe= RecipePlan.objects.filter(plan=get_first_plan.id).order_by("order")

        Weekly_Plan = []
        for day in day_name:
            Daily_recipes = []
            Single_day = {}
            for item in plan_recipe:
                if item.day_name.name == day.name:
                    Daily_recipes.append(item)

            Single_day[day.name] = Daily_recipes
            Weekly_Plan.append(Single_day)



        ctx = {"plans_number": plans_number, "recipes_number": recipes_number,
               "plan_name": get_first_plan, "Weekly_Plan": Weekly_Plan}

        return render(request,'dashboard.html', ctx)


class PlanList(View):

    def get(self,request):
        sorted_plans=Plan.objects.order_by("name")
        paginator = Paginator(sorted_plans, 50)

        page = request.GET.get('page')
        sorted = paginator.get_page(page)

        ctx = {"plans": sorted}
        return render(request, 'app-schedules.html',ctx)

class AddRecipe(View):

    def get(self,request):

        if "field_bad" in request.session:

            null_fields="wypełnij poprawnie wszystkie pola"

            ctx={"null_field":null_fields}

            del request.session["field_bad"]

            return render(request,'app-add-recipe.html',ctx)

        return render(request,'app-add-recipe.html')


    def post(self,request):
        recipe_name=request.POST.get("recipe_name")
        recipe_description = request.POST.get("recipe_description")
        preparation_time = request.POST.get("preparation_time")
        recipe_preparation = request.POST.get("recipe_preparation")
        recipe_ingredients = request.POST.get("recipe_ingredients")

        if (recipe_name and recipe_description and preparation_time and
            recipe_preparation and recipe_ingredients) is not "":

            new_recipe=Recipe.objects.create(name=recipe_name,description=recipe_description,
                                             preparation_time=preparation_time,preparation=recipe_preparation,ingredients=recipe_ingredients,votes=0)

            return redirect("/recipe/list")

        request.session["field_bad"]=True
        return redirect("/recipe/add")

class PlanId(View):

    def get(self,request,id):
        plan_details = Plan.objects.get(pk=id)
        plan_recipe = RecipePlan.objects.filter(plan=id).order_by("order")
        days = DayName.objects.all().order_by("order")

        Weekly_Plan = []

        for day in days:

            Daily_recipes = []
            Single_day = {}

            for item in plan_recipe:

                if item.day_name.name == day.name:
                    Daily_recipes.append(item)

            Single_day[day.name] = Daily_recipes
            Weekly_Plan.append(Single_day)

        ctx = {"plan_name": plan_details, "Weekly_Plan": Weekly_Plan,"plan_recipe":plan_recipe}


        return render(request,"app-details-schedules.html",ctx)

class AddPlan(View):

    def get(self,request):

        if "field_bad" in request.session:
            null_fields="wypełnij poprawnie wszystkie pola"
            ctx={"null_field":null_fields}
            del request.session["field_bad"]
            return render(request,'app-add-schedules.html',ctx)
        return render(request,'app-add-schedules.html')


    def post(self,request):
        plan_name=request.POST.get("planName")
        plan_description = request.POST.get("planDescription")
        if (plan_name and plan_description) is not "":
            new_plan=Plan.objects.create(name=plan_name,description=plan_description)
            request.session["plan_id"]=new_plan.pk
            return redirect("/plan/add/details")

        request.session["field_bad"]=True
        return redirect("/plan/add")


class RecipeDetails(View):
    def get(self,request, id):

        recipeID_valid = False

        try:
            recipe = Recipe.objects.get(pk=id)
            recipeID_valid = True
            ingredients_arr = []
            recipe_ingr = recipe.ingredients.split(", ")
            for ingr in recipe_ingr:
                ingredients_arr.append(ingr)

            ctx = {"recipe": recipe, "ingredients_arr": ingredients_arr, "recipeIsValid": recipeID_valid}

        except ObjectDoesNotExist as e:
            recipeID_valid = False
            error = "Brak przepisu dla ID: {}".format(id)
            ctx = { "recipeIsValid": recipeID_valid, "error" : error }

        return render(request, 'app-recipe-details.html', ctx)

    def post(self, request, id):

        try:
            recipe = Recipe.objects.get(pk=id)
            like=request.POST.get("like")
            dislike=request.POST.get("dislike")
            if like is not None:
                recipe.votes += 1
            elif dislike is not None:
                recipe.votes -= 1
            recipe.save()
            return redirect("/recipe/{}".format(id))
        except Exception as e:
            recipeID_valid = False
            error = "Błąd!!! {}".format(id)
            ctx = { "recipeIsValid": recipeID_valid, "error" : error }
            return render(request,'app-recipe-details.html',ctx)

class AddPlanDetails(View):

    def get(self,request):
        if "plan_id" in request.session:
            plan_id= request.session['plan_id']
            plan_name=Plan.objects.all()
            recipe_name = Recipe.objects.all()
            day_name=DayName.objects.all()

            ctx= {"plan_id": plan_id,"plan_name" : plan_name, "recipe_name" : recipe_name, "day_name" : day_name}
            return render(request, "app-schedules-meal-recipe.html",ctx)

        return HttpResponseForbidden("Error403-Access to this resource on the derver is denied!")

    def post(self,request):
        if "plan_id" in request.session:
            plan_id= request.session['plan_id']
            plan_name=Plan.objects.all()
            recipe_name = Recipe.objects.all()
            day_name=DayName.objects.all()

            ctx= {"plan_id": plan_id,"plan_name" : plan_name, "recipe_name" : recipe_name, "day_name" : day_name}
            return render(request, "app-schedules-meal-recipe.html",ctx)
        return HttpResponseForbidden("Error403-Access to this resource on the server is denied!")
      
class ModifyRecipe(View):
    def get(self, request,id):
        recipe=get_object_or_404(Recipe,id=id)
        ctx={"recipe" : recipe}
        if "field_bad" in request.session:
            null_fields = "Wypełnij poprawnie wszystkie pola"
            ctx = {"null_field": null_fields}
            del request.session["field_bad"]
            return render(request, 'app-edit-recipe.html', ctx)
        return render(request, 'app-edit-recipe.html',ctx)

    def post(self, request,id):
        recipe_name = request.POST.get("recipe_name")
        recipe_ingredients = request.POST.get("recipe_ingredients")
        recipe_description = request.POST.get("recipe_description")
        preparation_time = request.POST.get("preparation_time")
        recipe_preparation = request.POST.get("recipe_preparation")

        if (recipe_name and recipe_ingredients and recipe_description and preparation_time and
            recipe_preparation) is not "":
            modify_recipe = Recipe.objects.create(name=recipe_name, ingredients=recipe_ingredients,
                                                  description=recipe_description,
                                                  preparation_time=preparation_time, preparation=recipe_preparation,
                                                  votes=0)
            return redirect("/recipe/list")

        request.session["field_bad"] = True
        return redirect("/recipe/modify/{}".format(id))



