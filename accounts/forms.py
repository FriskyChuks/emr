from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
	"""
	A form for creating new users. Includes all the required
	fields, plus a repeated password.
	"""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username','first_name', 'last_name','other_names', 'email')

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserAdminCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserAdminChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('username', 'password', 'active', 'admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]


# class GuestForm(forms.Form):
# 	email = forms.EmailField(
# 							widget=forms.EmailInput(
# 					attrs={
# 					"class": "form-control", 
# 					"placeholder": "Enter Guest email"
# 					}))


class LoginForm(forms.Form):
	username = forms.CharField(
							widget=forms.TextInput(
					attrs={
					"class": "form-control", 
					"placeholder": "Enter your username"
					}))
	password = forms.CharField(
				widget=forms.PasswordInput(
					attrs={
					"class": "form-control", 
					"placeholder": "Enter password"
					}))

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username=username)
		if len(qs) < 1:
			raise forms.ValidationError('This USER does not exit!')
		return username 

	def clean_password(self):
		username_var = self.cleaned_data.get("email")
		password_var = self.cleaned_data.get("password")
		try:
			user = User.objects.get(email=username_var)
		except:
			user = None
		if user is not None and not user.check_password(password_var):
			raise forms.ValidationError("Wrong password!")
		elif user is None:
			pass
		else:
			return password_var


class RegisterForm(forms.ModelForm):
	"""
	A form for creating new users. Includes all the required
	fields, plus a repeated password.
	"""
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(label="Password Confirmation",\
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('first_name', 'last_name','other_names', 'username', 'email')

		widgets = {
		'first_name': forms.TextInput(attrs={'class': 'form-control'}),
		'last_name': forms.TextInput(attrs={'class': 'form-control'}),
		'other_names': forms.TextInput(attrs={'class': 'form-control'}),
		'username': forms.TextInput(attrs={'class': 'form-control'}),
		'email': forms.EmailInput(attrs={'class': 'form-control'}),
		'email': forms.EmailInput(attrs={'class': 'form-control'}),		
        }

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2
		
	def save(self, commit=True):
		# save the provided password in hashed format
		user = super(RegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.active=True
		if commit:
			user.save()
		return user
			

# class RegisterForm(forms.Form):
# 	username = forms.CharField(
# 				widget=forms.TextInput(
# 					attrs={
# 					"class": "form-control", 
# 					"placeholder": "Enter username"
# 					}))
# 	email = forms.EmailField(
# 							widget=forms.EmailInput(
# 					attrs={
# 					"class": "form-control", 
# 					"placeholder": "Enter your email"
# 					}))
# 	password = forms.CharField(
# 				widget=forms.PasswordInput(
# 					attrs={
# 					"class": "form-control", 
# 					"placeholder": "Enter password"
# 					}))
# 	password2 = forms.CharField(
# 				widget=forms.PasswordInput(
# 					attrs={
# 					"class": "form-control", 
# 					"placeholder": "Enter password"
# 					}))

# 	def clean_username(self):
# 		username = self.cleaned_data.get('username')
# 		qs = User.objects.filter(username=username)
# 		if qs.exists():
# 			raise forms.ValidationError('username already taken!, try something else pls')
# 		return username

# 	def clean_email(self):
# 		email = self.cleaned_data.get('email')
# 		qs = User.objects.filter(email=email)
# 		if qs.exists():
# 			raise forms.ValidationError('Email already taken!, try something else pls')
# 		return email


# 	def clean(self):
# 		data = self.cleaned_data
# 		password = self.cleaned_data.get('password')
# 		password2 = self.cleaned_data.get('password2')
# 		if password2 != password:
# 			raise forms.ValidationError("Passwords must match")
# 		else:
# 			return data


class ContactForm(forms.Form):
	Fullname = forms.CharField(
				widget=forms.TextInput(
					attrs={
					"class": "form-control", 
					"placeholder": "Enter Full Name"
					}))
	Email	 = forms.EmailField(
							widget=forms.EmailInput(
					attrs={
					"class": "form-control", 
					"placeholder": "Enter your email"
					}))
	Content  = forms.CharField(
				widget=forms.Textarea(
					attrs={
					"class": "form-control", 
					"placeholder": " Place your contents here"
					}))


	def clean_Email(self):
		Email = self.cleaned_data.get("Email")
		if not "@" in Email:
			raise forms.ValidationError("You must use Gmail")
		return Email

	def clean_Content(self):
		Content = self.cleaned_data.get("Content")
		if not "g" in Content:
			raise forms.ValidationError("please apply g")
		return Content