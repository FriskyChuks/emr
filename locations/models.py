from django.urls import reverse
from django.db import models


class Clinic(models.Model):
    clinic          = models.CharField(max_length=100, blank=False, null=False)
    female_only     = models.BooleanField(default=False)
    date_created    = models.DateField(auto_now_add=True, auto_now=False)
    updated         = models.DateField(auto_now_add=False, auto_now=True)
    active          = models.BooleanField(default=True)
    created_by      = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        ordering = ('clinic', )

    def __str__(self):
        return self.clinic

    def get_absolute_url(self):
        return reverse("clinic_detail_view", kwargs={"id": self.id})


class Ward(models.Model):
    clinic          = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    ward          = models.CharField(max_length=100, blank=False, null=False)
    female_only     = models.BooleanField(default=False)
    date_created    = models.DateField(auto_now_add=True, auto_now=False)
    updated         = models.DateField(auto_now_add=False, auto_now=True)
    active          = models.BooleanField(default=True)
    created_by      = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        ordering = ('ward',)

    def __str__(self):
        return self.ward


    def get_absolute_ward_url(self):
        return reverse("ward_detail_view", kwargs={"id": self.id})