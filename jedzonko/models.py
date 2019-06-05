from django.db import models


# Create your models here.

# - **recipe**: Tabela zawierająca przepisy.
#   - id: klucz główny tabeli,
#   - name: nazwa przepisu, varchar(255)
#   - ingredients: składniki przepisu, text
#   - description: treść przepisu, text
#   - created: data dodania przepisu (powinna być wypełniana automatycznie), timestamp with timezone
#   - updated: data aktualizacji przepisu (powinna być wypełniana automatycznie), timestamp with timezone
#   - preparation_time: czas przygotowania (w minutach), integer
#   - preparation: sposób przygotowania
#   - votes: liczba głosów na przepis, integer

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateField(auto_now_add = True)
    updated = models.DateField(auto_now = True)
    preparation_time = models.IntegerField()
    preparation = models.TextField()
    votes = models.IntegerField()

# - **plan**: Tabela zawierająca informacje na temat planów.
#   - id: klucz główny tabeli,
#   - name: nazwa planu, varchar(255)
#   - description: opis planu, text
#   - created: data utworzenia. timestamp with timezone

class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateField(auto_now_add = True)

#
# - **dayname**: Tabela zawierająca nazwy dni (podejmijcie decyzję projektową: zastanówcie się, czy nie lepiej zamienić to na enuma w Django)
#   - id: klucz główny tabeli,
#   - name: nazwa dnia, varchar(16)
#   - order: kolejność dnia, integer

class DayName(models.Model):
    name = models.CharField(max_length=16, unique=True)
    order = models.SmallIntegerField(unique=True)

# - **page**: Tabela zawierająca dane strony.
#   - id: klucz główny tabeli,
#   - title: tytuł strony, varchar(255)
#   - descritption: treść strony, text
#   - slug: unikalny identyfikator tworzony na podstawie tytułu, varchar(255)

class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.CharField(max_length=255)

#
# - **recipeplan**: Tabela zawierająca informacje o połączeniu przepisu oraz planu.
#   - id: klucz główny tabeli,
#   - meal_name: nazwa posiłku, varchar(255)
#   - recipe_id: klucz obcy do tabeli przepisów (w modelu nazwij to „recipe”),
#   - plan_id: klucz obcy do tabeli planów (w modelu nazwij to „plan”),
#   - order: kolejność posiłków w planie, integer
#   - day_name_id: klucz obcy z do tabeli day_name (w modelu nazwij to „day_name”)

class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    order = models.SmallIntegerField()
    recipe = models.ForeignKey('Recipe', on_delete=models.DO_NOTHING, blank=True, null=True)
    plan = models.ForeignKey('Plan', on_delete=models.DO_NOTHING, blank=True, null=True)
    day_name = models.ForeignKey('DayName', on_delete=models.DO_NOTHING, blank=True, null=True)

