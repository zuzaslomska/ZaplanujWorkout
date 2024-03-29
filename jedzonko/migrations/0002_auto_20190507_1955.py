# Generated by Django 2.0 on 2019-05-07 17:55

from django.db import migrations

def add_DayNames(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    DayName = apps.get_model('jedzonko', 'DayName')

    Days = {
    "Monady" : 8,
    "Thusday" : 9,
    "Wensday" : 10,
    "Thursday" : 11,
    "Friday": 12,
    "Saturday": 13,
    "Sunday" : 14
    }
    for key, value in Days.items():
        DayName.objects.create(name=key, order=value)

def add_Plans(apps, schema_editor):

    Plan = apps.get_model('jedzonko', 'Plan')

    Norway = {
        "name" : "Dieta Norweska",
        "description" : """Opracowana przez lekarzy i specjalistów żywienia w Oslo.
        Zakłada restrykcyjną dietę trwającą 14 dni. Podstawą diety norweskiej są jajka i grejpfruty - muszą być w codziennym jadłospisie.
        Poza tym można jeść wybrane owoce i warzywa oraz gotowane mięso.
        W dwa tygodnie można schudnąć 10 kilogramów"""
    }

    Plan.objects.create(name=Norway["name"], description=Norway["description"])

    Espaniol = {
        "name" : "Dieta hiszpańska",
        "description" : """Polega na obniżeniu spożycia kalorii - dziennie do 1000-1500 kcal.
        Oparta jest na owcach i warzywach. Zakłada zrzucenie 3-6 kilogramów w ciągu dwóch tygodni diety"""
    }

    Plan.objects.create(name=Espaniol["name"], description=Espaniol["description"])

def add_Recipes(apps, schema_editor):

    Recipe = apps.get_model('jedzonko','Recipe')

    Recipe.objects.create(
    name="Śnidanie po Norwesku",
    ingredients="3 jajka, kawa",
    description="Gotowane jajka z kawą bez mleka i cukru",
    preparation_time=5,
	preparation="gotuj jajka 2 minuty",
    votes=2)

    Recipe.objects.create(
    name="Norweski obiad",
    ingredients="2 jajka, porcja szpinaku, jogurt",
    description="Jajka ze szpinakiem z dodatkiem jogurtu naturalnego",
    preparation_time=15,
	preparation="zagotuj jajka, dodaj porcję szpinaku i jogurtu wedle uznania",
    votes=20)

    Recipe.objects.create(
    name="Hiszpańskie śniadanie",
    ingredients="kawa bez cukru, 2 kromki pieczywa chrupkiego, 2 plasterki polędwicy drobiowej, jogurt beztłuszczowy naturalny",
    description="Pieczywo chrupkie z polędwicą",
    preparation_time=5,
	preparation="zrób kanapki z przygotowanych składników",
    votes=25)

    Recipe.objects.create(
    name="Obiad po Hiszpańsku",
    ingredients="300 g warzyw z patelni (smażonych na oliwie z oliwek), jogurt naturalny",
    description="Smażone warzywa",
    preparation_time=20,
	preparation="Smaż warzywa na patelni i dolej do nich jogurt naturalny",
    votes=35)

    Recipe.objects.create(
    name="Hiszpańska Kolacja",
    ingredients="sałatka pomidorowa polana sosem winegret, 2 plasterki szynki z indyka, pieczone jabłko",
    description="Sałatka pomidorowa",
    preparation_time=20,
	preparation="Wszystkie składniki wrzuć do jednego naczynia i smacznego",
    votes=60)

# class RecipePlan(models.Model):
#     meal_name = models.CharField(max_length=255)
#     order = models.SmallIntegerField(unique=True)
#     recipe = models.ForeignKey('Recipe', on_delete=models.DO_NOTHING)
#     plan = models.ForeignKey('Plan', on_delete=models.DO_NOTHING)
#     day_name = models.ForeignKey('DayName', on_delete=models.DO_NOTHING)

def add_RecipePlans(apps, schema_editor):

    Recipe = apps.get_model('jedzonko','Recipe')
    DayName = apps.get_model('jedzonko', 'DayName')
    Plan = apps.get_model('jedzonko', 'Plan')
    RecipePlan = apps.get_model('jedzonko', 'RecipePlan')

    r1_1 = RecipePlan.objects.create(
    meal_name="r1 sniadanie",
    order=1,
    plan = Plan.objects.get(pk=1),
    recipe = Recipe.objects.get(pk=1),    #Śnidanie po Norwesku
    day_name = DayName.objects.get(pk=1)
    )

    r1_2 = RecipePlan.objects.create(
    meal_name="r1 obiad",
    order=2,
    plan = Plan.objects.get(pk=1),
    recipe = Recipe.objects.get(pk=2),     #Norweski obiad
    day_name = DayName.objects.get(pk=1),
    )

    r2_1 = RecipePlan.objects.create(
    meal_name="r2 śniadanie",
    order=1,
    plan = Plan.objects.get(pk=2),
    recipe = Recipe.objects.get(pk=3),     #Hiszpańskie śniadanie
    day_name = DayName.objects.get(pk=2),
    )

    r2_2 = RecipePlan.objects.create(
    meal_name="r2 obiad",
    order=2,
    plan = Plan.objects.get(pk=2),
    recipe = Recipe.objects.get(pk=4),     #Obiad po Hiszpańsku
    day_name = DayName.objects.get(pk=2)
    )

    r2_3 = RecipePlan.objects.create(
    meal_name="r2 kolacja",
    order=3,
    plan = Plan.objects.get(pk=2),
    recipe = Recipe.objects.get(pk=5),     #Hiszpańska Kolacja
    day_name = DayName.objects.get(pk=2)
    )

class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_DayNames),
        migrations.RunPython(add_Plans),
        migrations.RunPython(add_Recipes),
        migrations.RunPython(add_RecipePlans),
    ]
