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
					Q(id__iexact=query)|
					Q(first_name__icontains=query)| 
					Q(last_name__icontains=query) |
					Q(date_of_birth__iexact=query)|
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


COUNTRY = (
		('nigeria', 'Nigeria'),
	)

STATE = (
			('lagos', 'Lagos'),
			('nasarawa', 'Nasarawa'),
			('abia', 'Abia'),
			('adamawa', 'Adamawa'),
			('anambra', 'Anambra'),
			('akwa-ibom', 'Akwa-Ibom'),
			('delta', 'Delta'),
			('edo', 'Edo'),
			('enugu', 'Enugu'),
			('jigawa', 'Jigawa'),
			('ondo', 'Ondo'),
			('imo', 'Imo'),
			('bauchi', 'Bauchi'),
			('plateau', 'Plateau'),
			('ogun', 'Ogun'),
			('kaduna', 'Kaduna'),
			('katsina', 'Katsina'),
			('sokoto', 'Sokoto'),
			('osun', 'Osun'),
			('benue', 'Benue'),
			('kogi', 'Kogi'),
			('fct(Abuja)', 'FCT(Abuja)'),
			('ebonyi', 'Ebonyi'),
			('cross-rivers', 'Cross-Rivers'),
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
		('son', 'Son'),
	)


# class State(models.Model):
# 	state = models.CharField(max_length=20, choices=STATE, unique=True)
# 	country = models.CharField(max_length=50)

# 	def __str__(self):
# 		return str(self.state)


# class LGA(models.Model):
# 	state = models.ForeignKey(State, on_delete=models.CASCADE)
# 	lga   = models.CharField(max_length=50)

# 	def __str__(self):
# 		return str(self.lga)


class Patient(models.Model):
	foto			= models.ImageField(null=True, blank=True, upload_to="image/", default="image/male.jpg")
	first_name      = models.CharField(max_length=50)
	last_name       = models.CharField(max_length=50)
	other_names     = models.CharField(max_length=50)
	gender          = models.CharField(max_length=10, choices=GENDER)
	date_of_birth   = models.DateField()
	marital_status  = models.CharField(max_length=10, choices=MARITAL_STATUS)
	phone_1         = models.CharField(max_length=11, unique=True)
	phone_2         = models.CharField(max_length=11, null=True, blank=True)
	country         = models.CharField(max_length=100, choices=COUNTRY, default="Nigeria")
	state           = models.CharField(max_length=100, choices=STATE, default='nasarawa')
	l_g_a           = models.CharField(max_length=100, default='keffi')
	address         = models.TextField(null=True, blank=True)
	next_of_kin_relationship  = models.CharField(max_length=50, choices=RELATIONSHIP)
	full_name           = models.CharField(max_length=150)
	phone               = models.CharField(max_length=11)
	next_of_kin_address = models.TextField()
	date_created    = models.DateTimeField(auto_now_add=True, auto_now=False)
	last_updated    = models.DateTimeField(auto_now_add=False, auto_now=True)
	new		          = models.BooleanField(default=True)
	active          = models.BooleanField(default=True)
	created_by      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

	objects = PatientManager()

	def __str__(self):
		return f"{self.first_name} {self.last_name}"


	def get_absolute_url(self):
		return reverse("patient_detail", kwargs={"id": self.id})

	class Meta:
		unique_together = ('first_name', 'last_name', 'date_of_birth')