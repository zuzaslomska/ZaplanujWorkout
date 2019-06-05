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
from jedzonko.views import IndexView, About, Contact, RecipesList,PlanList,\
    LandingPage, MainPage, AddRecipe,AddPlan, RecipeDetails, AddPlanDetails,PlanId,Main,\
    ModifyRecipe


urlpatterns = [
    path('index/', IndexView.as_view()),

    path('about/', About.as_view()), 
    path('contact/', Contact.as_view()), 
    path('main/', IndexView.as_view()),
    path('recipe/list/', RecipesList.as_view()),
    path('', LandingPage.as_view()),
    path('main/', MainPage.as_view()),
    path('recipe/<int:id>/', RecipeDetails.as_view()),
    path('recipe/add/', AddRecipe.as_view()),
    path('recipe/modify/<id>/',ModifyRecipe.as_view()),
    path('plan/list/',PlanList.as_view()),
    path('plan/<int:id>/',PlanId.as_view()),
    path('plan/add/', AddPlan.as_view()),
    path('plan/add/details/', AddPlanDetails.as_view()),
    path('about/', About),
    path('contact/', Contact),
]
