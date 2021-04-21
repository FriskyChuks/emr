from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class LabUnit(models.Model):
    title        = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description  = models.CharField(max_length=255, blank=True, null=True)
    created_by   = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated      = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title


class CompoundTest(models.Model):
    lab_unit            = models.ForeignKey(LabUnit, on_delete=models.CASCADE, blank=True, null=True)
    title               = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description         = models.CharField(max_length=255, blank=True, null=True)
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created        = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title


class LabTest(models.Model):
    lab_unit            = models.ForeignKey(LabUnit, on_delete=models.CASCADE, blank=True, null=True)
    compound_test       = models.ForeignKey(CompoundTest, on_delete=models.CASCADE, blank=True, null=True)
    title               = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description         = models.CharField(max_length=255, blank=True, null=True)
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created        = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated             = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

