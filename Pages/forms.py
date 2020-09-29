from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User_Model=get_user_model()

# <-------------- authentication -------------->

class LoginForm(forms.Form):
	username=forms.CharField(
		required=True,
		widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'e.g: Jamshid98',
			}
		)
	)
	password=forms.CharField(
		required=True,
		widget=forms.PasswordInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'e.g: qwerty123',
			}
		)
	)

# Override the UserCreationForm
class RegisterForm(UserCreationForm, forms.Form):
	username=forms.CharField(
		required=True,
		widget=forms.TextInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'e.g: Jamshid'
			}
		)
	)
	email=forms.EmailField(
		required=True,
		widget=forms.EmailInput(
			attrs={
				'class' : 'form-control',
				'placeholder' : 'e.g: example@example.com',
			}
		)
	)
	password1=forms.CharField(
		max_length=10,
		min_length=8, 
		required=True,
		label='Password',
		widget=forms.PasswordInput(
			attrs={
				'class' : 'from-control',
				'placeholder' : 'Create Password',
			}
		)	
	)
	password2=forms.CharField(
		max_length=10,
		min_length=8, 
		required=True,
		label='Password',
		widget=forms.PasswordInput(
			attrs={
				'class' : 'from-control',
				'placeholder' : 'Confirm Password',
			}
		)	
	)

	def clean(self):
		cleaned_data=self.cleaned_data
		password_1=self.cleaned_data.get('password1')
		password_2=self.cleaned_data.get('password2')
		if password_1 != password_2:
			raise forms.ValidationError("Password didn't match. Try agoin")
		return cleaned_data
	
	def clean_username(self):
		username=self.cleaned_data.get('username')
		queryset=User_Model.objects.filter(username=username)
		if queryset.exists():
			raise forms.ValidationError("Username  you've chosen is unavailable. Try different one")
		return username
	
	def clean_email(self):
		email_address=self.cleaned_data.get('email')
		queryset=User_Model.objects.filter(email=email_address)
		if queryset.exists():
			raise forms.ValidationError('The email address you\'ve chosen is already registered.')
		return email_address

	class Meta:
		model=User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

# <-------------- authentication -------------->

# <-------------- contact -------------->

def should_be_empty(value):
    if value:
        raise forms.ValidationError('Field is not empty')


class ContactForm(forms.Form):
    name = forms.CharField(
		max_length=80,
		required=True,
		widget=forms.TextInput(
			attrs={
				'id' : 'id_name',
				'placeholder' : 'Enter your name here'
			}
		)
	)
    message = forms.CharField(
		required=True,
		widget=forms.Textarea(
			attrs={
				'id' : 'id_message',
				'placeholder' : 'Enter your message',
			}
		)
	)
    email = forms.EmailField(
		required=True,
		widget=forms.EmailInput(
			attrs={
				'id' : 'id_email',
				'placeholder' : 'Enter your valid e-mail address'
			}
		)
	)
    forcefield = forms.CharField(
        required=False, 
		widget=forms.HiddenInput, 
		label="Leave empty", 
		validators=[should_be_empty]
	)

# <-------------- contact -------------->