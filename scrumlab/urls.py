"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from jedzonko.views import IndexView, HomePageView, RecipesPageView, MainPageView, RecipeDetailsView, AddRecipeView,\
    RecipeEditView, PlanDetailsView, PlanListView, PlanAddView, AddRecipeToPlanView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('', HomePageView.as_view(), name='landing-page'),
    path('main/', MainPageView.as_view(), name='dashboard'),
    path('plan/<int:id>/', PlanDetailsView.as_view(), name='plan-details'),
    path('plan/add/', PlanAddView.as_view(), name='plan-add'),
    path('plan/list/', PlanListView.as_view(), name='plans'),
    path('recipe/<int:id>/', RecipeDetailsView.as_view()),
    path('recipe/add/', AddRecipeView.as_view(), name='recipe-add'),
    path('recipe/list/', RecipesPageView.as_view(), name='recipes'),
    path('recipe/modify/<int:id>/', RecipeEditView.as_view()),
    path('plan/add-recipe/', AddRecipeToPlanView.as_view(), name='recipe-add-to-plan'),
]
