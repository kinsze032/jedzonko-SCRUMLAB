from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound

from django.shortcuts import render, redirect
from django.views import View
from jedzonko.models import Recipe, Plan, RecipePlan, DayName

import random


class IndexView(View):
    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class HomePageView(View):
    def get(self, request):
        all_recipe = list(Recipe.objects.all())
        random.shuffle(all_recipe)
        if len(all_recipe) >= 3:
            context = {"recipe_1": all_recipe[0], "recipe_2": all_recipe[1], "recipe_3": all_recipe[2]}
        if len(all_recipe) == 2:
            context = {"recipe_1": all_recipe[0], "recipe_2": all_recipe[1]}
        if len(all_recipe) == 1:
            context = {"recipe_1": all_recipe[0]}
        if len(all_recipe) == 0:
            return render(request, "index.html")

        return render(request, "index.html", context)


class MainPageView(View):
    def get(self, request):
        last_plan = Plan.objects.all().order_by("-created").first()
        recipe_plan = RecipePlan.objects.filter(plan=last_plan)
        days_list = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
        context = {"lastPlan": last_plan,
                   "recipe_plan": recipe_plan,
                   "days_list": days_list
                   }
        return render(request, "dashboard.html", context)


class RecipesPageView(View):
    def get(self, request):
        recipes = Recipe.objects.all().order_by('votes').order_by('created')
        pagination = Paginator(recipes, 50)
        page_number = request.GET.get('page')
        pagination = pagination.get_page(page_number)
        return render(request, "app-recipes.html", {'page_obj': pagination})


class RecipeDetailsView(View):
    def get(self, request, id):
        try:
            Recipe.objects.get(pk=id)
            return render(request, "app-recipe-details.html")
        except ObjectDoesNotExist:
            return HttpResponseNotFound()


class AddRecipeView(View):
    def get(self, request):
        return render(request, "app-add-recipe.html")


class RecipeEditView(View):
    def get(self, request, id):
        try:
            Recipe.objects.get(pk=id)
            return render(request, "app-edit-recipe.html")
        except ObjectDoesNotExist:
            return HttpResponseNotFound()


class PlanDetailsView(View):
    def get(self, request, id):
        return render(request, "app-details-schedules.html")


class PlanListView(View):
    def get(self, request):
        # wersja z sortowaniem leksykalnym
        plans = Plan.objects.all().order_by('name')

        # sortowanie alfanumerycznie dla nazw "Nazwa planu 1", "Nazwa planu 2"
        # plans = Plan.objects.all().extra(select={
        #     'name_alpha': "regexp_replace(name, E'([^0-9]*)([0-9]*)([^0-9]*)', E'\\\\\\\\\\\\\1 \\\\\\\\\\\\\\2 \\\\\\\\\\\\\\3', 'g')"}).order_by(
        #     'name_alpha')
        pagination = Paginator(plans, 50)
        page_number = request.GET.get('page')
        pagination = pagination.get_page(page_number)
        return render(request, "app-schedules.html", {'page_obj': pagination})


class PlanAddView(View):
    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        planName = request.POST.get("planName")
        planDescription = request.POST.get("planDescription")

        if not planName:
            return render(
                request,
                "app-add-schedules.html",
                context={"error": "Nie podano nazwy planu"},
            )

        if not planDescription:
            return render(
                request,
                "app-add-schedules.html",
                context={"error": "Nie podano opisu planu"},
            )

        if Plan.objects.filter(name=planName):
            return render(
                request,
                "app-add-schedules.html",
                context={"error": "Plan o podanej nazwie już istnieje"},
            )

        Plan.objects.create(name=planName, description=planDescription)
        plan = Plan.objects.get(name=planName)
        return redirect('plan-details', plan.id)


class AddRecipeToPlanView(View):
    def get(self, request):
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        context = {
            'plans': plans,
            'recipes': recipes
        }
        return render(request, "app-schedules-meal-recipe.html", context)

    def post(self, request):
        meal_name = request.POST.get("meal_name")
        order = request.POST.get("order")
        day_name = request.POST.get("day_name")
        for num in DayName.DayChoices:
            if num.label == day_name:
                day_obj = DayName.objects.filter(day_name_to_do=num.value).first()
                break
        plan_name = request.POST.get("plan_name")
        plan_obj = Plan.objects.filter(name=plan_name).first()
        recipe_name = request.POST.get("recipe_id")
        recipe_obj = Recipe.objects.filter(name=recipe_name).first()
        RecipePlan.objects.create(
            meal_name=meal_name, order=order, day_name=day_obj, plan=plan_obj, recipe=recipe_obj
        )
        return redirect('plan-details', plan_obj.id)
