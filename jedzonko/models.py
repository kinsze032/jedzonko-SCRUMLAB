from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.



class Recipe(models.Model):
    VOTES_CHOICES = {
        (0, 'Bad'),
        (1, '*'),
        (2, '**'),
        (3, '***'),
        (4, '****'),
        (5, '*****')
    }
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    ingredient = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.TimeField()
    votes = models.PositiveSmallIntegerField(choices=VOTES_CHOICES, default=0)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through="RecipePlan")


class DayName(models.Model):
    class DayChoices(models.IntegerChoices):
        CHOOSE_DAY = 0, _('Wybierz dzień')
        MONDAY = 1, _('Poniedziałek')
        TUESDAY = 2, _('Wtorek')
        WEDNESDAY = 3, _('Środa')
        THURSDAY = 4, _('Czwartek')
        FRIDAY = 5, _('Piątek')
        SATURDAY = 6, _('Sobota')
        SUNDAY = 7, _('Niedziela')

    day_name_to_do = models.IntegerField(
        choices=DayChoices.choices,
        default=DayChoices.CHOOSE_DAY)


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255, unique=True)
    order = models.IntegerField()
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.CharField(max_length=255)
