from django.db.models import Q
from django.db.models.expressions import F
from django.urls import reverse
from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

User = settings.AUTH_USER_MODEL


class PatientQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    # def featured(self):
    # 	return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (
            Q(id__iexact=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(date_of_birth__iexact=query) |
            Q(phone_1__iexact=query)
        )
        return self.filter(lookups).distinct()


class PatientManager(models.Manager):
    def search(self, query):
        return self.get_queryset().active().search(query)

    def get_queryset(self):
        return PatientQuerySet(self.model, using=self._db)


MARITAL_STATUS = (
    ('single', 'Single'),
    ('married', 'Married'),
    ('divorced', 'Divorced'),
)


GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
)

RELATIONSHIP = (
    ('spouse', 'Spouse'),
    ('brother', 'Brother'),
    ('sister', 'Sister'),
    ('father', 'Father'),
    ('mother', 'Mother'),
    ('cousin', 'Cousin'),
    ('nephew', 'Nephew'),
    ('niece', 'Niece'),
    ('uncle', 'Uncle'),
    ('aunt', 'Aunt'),
    ('neighbour', 'Neighbour'),
    ('son', 'Son'),
    ('daughter', 'Daughter'),
)


class Relationship(models.Model):
    title = models.CharField(max_length=100,  unique=True)

    def __str__(self):
        return str(self.title)


class Continent(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.title)


class Country(models.Model):
    title = models.CharField(max_length=50, unique=True)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class State(models.Model):
    title = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)


class LGA(models.Model):
    title = models.CharField(max_length=50, unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)


class Patient(models.Model):
    foto = models.ImageField(null=True, blank=True, upload_to="users/")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    other_names = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS)
    phone_1 = models.CharField(max_length=11, unique=True)
    phone_2 = models.CharField(max_length=11, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    l_g_a = models.ForeignKey(LGA, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    next_of_kin_relationship = models.ForeignKey(
        Relationship, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=11)
    next_of_kin_address = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    new = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    objects = PatientManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("patient_detail", kwargs={"id": self.id})

    class Meta:
        unique_together = ('first_name', 'last_name', 'date_of_birth')
