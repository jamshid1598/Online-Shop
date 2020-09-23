from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import View

# from django.contrib.auth.forms import  AuthenticationForm  # Now we can use 'LoginForm' instead of 'AuthenticationForm'
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse 
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import login_required
# from .decorators import unauthenticated_user, allowed_users, admin_only

from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
)


from .forms import (
	# NewUserForm,
	LoginForm,
	RegisterForm,
	ContactForm,

	CategoryCreate,
	ProductCreate,
)

from .models import (
    Category,
    Product,
	ProductImage,
)



# << -------------------  AuthenticationForm Function ------------------------>
@csrf_protect
@unauthenticated_user
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


@unauthenticated_user
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
				return redirect("Product:product-list")
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
	return redirect("Product:product-list")

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
            # return HttpResponse('Success...Your email has been sent')
	form = ContactForm()
	return render(
		request=request, 
		template_name="Pages/contact.html", 
		context={'form': form, 'msg':msg}
	)

# << -------------------  ContactForm Function ------------------------>>

# <-------------- class based Product-List view -------------->
class Product_List_View(View):
    # template_name='Product/product-list.html'
	template_name='ProductPages/product-list.html'
	context={}
	model=Category
	look_up='id'
	def get_object(self):
		id=self.kwargs.get(self.look_up)
		if id is not None:
			product_category=get_object_or_404(self.model, id=id)
			print(product_category)
			queryset=product_category.product_name.all()
			return queryset
		elif len(Product.objects.all()) > 20:
			queryset_c=Category.objects.all()
			queryset_p=Product.objects.order_by('-published_at')[:21]
			return queryset_p, queryset_c
		else:
			queryset_c=Category.objects.all()
			queryset_p=Product.objects.all()
			return queryset_p, queryset_c

	def get(self, request, id=None, *args, **kwargs):
		object_list=None
		object_list_c=None
		if id is not None:
			object_list=self.get_object()
			self.context['object_list'] = object_list
			self.context['quantity'] = len(object_list)
		else:
			object_list, object_list_c =self.get_object()
			self.context['object_list'] = object_list
			self.context['object_list_c'] = object_list_c
		return render(
            request,
            self.template_name,
            self.context
        )
# <-------------- class based Product-List view -------------->

# <-------------- class based Product-Category-List view -------------->
class Category_Product_List_View(View):
	template_name='ProductPages/product-list.html'
	context={}
	model=Category
	look_up='id'
	def get_object(self):
		id=self.kwargs.get(self.look_up)
		product_category=get_object_or_404(self.model, id=id)
		print(product_category)
		queryset=product_category.product_name.all()
		return queryset
	def get(self, request, id=None, *args, **kwargs):
		object_list=self.get_object()
		self.context['object_list'] = object_list
		self.context['quantity'] = len(object_list)
		return render(
            request,
            self.template_name,
            self.context
        )
# <-------------- class based Product-Category-List view -------------->


class ProductObjectMixin(object):
    model=Product
    url_lookup='id'
    def get_object(self):
        obj=None
        id=self.kwargs.get(self.url_lookup)
        if id is not None:
            obj=get_object_or_404(self.model, id=id)
        return obj

# <-------------- class based Product-Detail view -------------->
class Product_Detail_View(ProductObjectMixin, View):
    template_name='ProductPages/product-detail.html'
    context={}
    def get(self, request, id=None, *args, **kwargs):
        obj=self.get_object()
        self.context['product'] = obj
        return render(
            request,
            self.template_name,
            self.context
        )
# <-------------- class based Product-Detail view -------------->

# <-------------- class based Product-Create-Update-Delete view -------------->
class Product_Create_View(View):
	template_name='ProductPages/product-create.html'
	context={}
	def get(self, request, *args, **kwargs):
		form=ProductCreate()
		self.context={ 'form' : form }
		return render(
            request,
            self.template_name,
            self.context,
	    )
	def post(self, request, *args, **kwargs):
		if request.method=="POST":
			form=ProductCreate(request.POST, request.FILES)
			if form.is_valid():
				form.save()
				form=ProductCreate()
		else:
			form=ProductCreate()
		self.context={ 'form' : form }
		return render(
			request,
			self.template_name,
			self.context,
		)


class Product_Update_View(ProductObjectMixin, View):
	template_name='ProductPages/product-update.html'
	context={}
	def get(self, request, id=None, *args, **kwargs):
		product=self.get_object()
		form=ProductCreate(instance=product)
		self.context={ 'form' : form , 'id':id}
		return render(
            request,
            self.template_name,
            self.context,
	    )
	def post(self, request, id=None, *args, **kwargs):
		if request.method=="POST":
			product=self.get_object()
			form=ProductCreate(request.POST, request.FILES, instance=product)
			if form.is_valid():
				form.save()
			# form=ProductCreate()
			# return HttpResponseRedirect(reverse('Product:product-detail', args=(product.id)))
		self.context={ 'form' : form, 'id':id}
		return render(
			request,
			self.template_name,
			self.context,
		)



class Product_Delete_View(ProductObjectMixin, View):
    template_name='ProductPages/product-delete.html'
    def get(self, request, id=None, *args, **kwargs):
        obj=self.get_object()
        context={}
        if obj is not None:
            context['product']=obj
        return render(
            request,
            self.template_name,
            context
        )

    def post(self, request, id=None, *args, **kwargs):
        obj=self.get_object()
        context={}
        if obj is not None:
            obj.delete()
            context['product']=None
            return redirect("Product:product-list")
        return render(
            request,
            self.template_name,
            context,
        )
# <-------------- class based Product-Detail-Update-Delete view -------------->