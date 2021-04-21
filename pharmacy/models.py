from django.db.models.enums import Choices
from django.urls import reverse
from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

User = settings.AUTH_USER_MODEL

from visits.models import PatientEncounter
from patients.models import Patient


CATEGORY = (
    ('drug','Drug'),
    ('consummables','Consummables'),
)

# DRUG_UNIT = (
#     ('grams','grams'),
#     ('milli-grams','milli-grams'),
#     ('milli-litres','milli-litres'),
#     ('litres','litres'),
# )


TYPE = (
    ('tab','Tab'),
    ('syrup','Syrup'),
    ('injectibles','Injectibles'),
    # ('syrup','Syrup'),
)


DRUG_ROUTE = (
    ('oral','Oral'),
    ('iv','IV'),
    # ('injectibles','Injectibles'),
    # ('syrup','Syrup'),
)

TIMES_DAILY = (
    ('bd','BD'),
    # ('iv','IV'),
    # ('injectibles','Injectibles'),
    # ('syrup','Syrup'),
)


class Item(models.Model):
    category        = models.CharField(max_length=50, choices=CATEGORY)
    title           = models.CharField(max_length=120)
    description     = models.TextField(null=True, blank=True)
    strength        = models.CharField(max_length=50)
    type            = models.CharField(max_length=100, choices=TYPE, blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated         = models.DateTimeField(auto_now_add=False, auto_now=True)
    active          = models.BooleanField(default=True)
    created_by      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return str(self.title) + " " + "(" +str(self.strength)+")" + " " + str(self.type)


    def get_absolute_url(self):
        return reverse("single_product", kwargs={"slug": self.slug})


class Brand(models.Model):
    item            = models.ForeignKey(Item, on_delete=models.CASCADE)
    title           = models.CharField(max_length=120)
    description     = models.TextField(null=True, blank=True)
    price           = models.DecimalField(max_digits=65, decimal_places=2, default=00.00)
    sale_price      = models.DecimalField(max_digits=65, decimal_places=2, default=00.00, null=True, blank=True)
    slug            = models.SlugField(unique=True, blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated         = models.DateTimeField(auto_now_add=False, auto_now=True)
    active          = models.BooleanField(default=True)
    created_by      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.title) + " " + str(self.item.title)

    class Meta:
        unique_together = ('title', 'slug')

    def get_absolute_url(self):
        return reverse("single_product", kwargs={"slug": self.slug})


class Prescription(models.Model):
    encounter_no        = models.ForeignKey(PatientEncounter, on_delete=models.CASCADE)
    patient             = models.ForeignKey(Patient, on_delete=models.CASCADE)
    item                = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty_per_take        = models.IntegerField()
    times_daily         = models.CharField(max_length=20, choices=TIMES_DAILY)
    no_of_days          = models.IntegerField()
    route               = models.CharField(max_length=20, choices=DRUG_ROUTE)
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    timestamp           = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.item.title) + " " + str(self.item.type)

    

