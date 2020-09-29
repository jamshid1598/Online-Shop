from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import View

# from django.contrib.auth.forms import  AuthenticationForm  # Now we can use 'LoginForm' instead of 'AuthenticationForm'
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.core.mail import send_mail, BadHeaderError
# from django.contrib.admin.views.decorators import staff_member_required

# from django.contrib.auth.decorators import login_required
# from .decorators import unauthenticated_user, allowed_users, admin_only


from .forms import (
	# NewUserForm,
	LoginForm,
	RegisterForm,
	ContactForm,
)

# from .models import (
#     Category,
#     Product,
# 	ProductImage,
# )



# << -------------------  AuthenticationForm Function ------------------------>
@csrf_protect
def register_request(request):
	if request.method == "POST":
		form = RegisterForm(request.POST or None)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, "New account created: {}".format(username))
			login(request, user)
			messages.info(request, "You are now loged in {}".format(username))
			return redirect("Product:product-list")
		else:
			for msg in form.errors:
				messages.error(request, f"{msg}: {form.errors[msg]}")

			return render(
				request,
				"Pages/register.html",
				context={
					'form' : form
				}
			)

	form = RegisterForm
	return render(
		request,
		"Pages/register.html",
		context={
			'form' : form
		}
	)


def login_request(request):
	if request.method == 'POST':
		form=LoginForm(request.POST or None)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, "you are now logged in as {}".format(username))
				return redirect("Products:product-list")
			else:
				messages.error(request, "invaled username or password")
		else:
			messages.error(request, "invaled username or password")

	form = LoginForm()
	return render(
			request=request,
			template_name="Pages/login.html",
			context={
				'form' : form
			}
		)


def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("Products:product-list")

# << -------------------  AuthenticationForm Function ------------------------>>

# << -------------------  ContactForm Function ------------------------>>

def contact_request(request, *args, **kwargs):
	form = ContactForm()
	msg=False
	if request.method == 'POST':
		form = ContactForm(request.POST or None)
		if form.is_valid():
			subject = f'Message from {form.cleaned_data["name"]}'
			message = form.cleaned_data["message"]
			sender = form.cleaned_data["email"]
			recipients = ['dovurovjamshid95@gmail.com']
			try:
				send_mail(subject, message, sender, recipients, fail_silently=True)
				msg=True
			except BadHeaderError:
				return HttpResponse('Invalid header found')
	form = ContactForm()
	return render(
		request=request, 
		template_name="Pages/contact.html", 
		context={'form': form, 'msg':msg}
	)

# << -------------------  ContactForm Function ------------------------>>