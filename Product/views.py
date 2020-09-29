from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import View

# from django.contrib.auth.forms import  AuthenticationForm  # Now we can use 'LoginForm' instead of 'AuthenticationForm'
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from django.core.mail import send_mail, BadHeaderError


# Class Based Views
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
)


from .forms import (
	CategoryCreate,
	ProductCreate,
)

from .models import (
    Category,
    Product,
	ProductImage,
)



# # << -------------------  ContactForm Function ------------------------>>

# <-------------- class based Product-List view -------------->
class Product_List_View(View):
    # template_name='Product/product-list.html'
	template_name='ProductPages/product-list.html'
	context={}
	model=Category
	look_up='id'
	def get_object(self):
		id=self.kwargs.get(self.look_up)
		
		queryset_products = Product.objects.all()
		queryset_category = Category.objects.all()

		if id is not None:
			queryset_category = get_object_or_404(self.model, id=id)
			queryset_products = queryset_category.product_name.all()

		return queryset_category, queryset_products

	def get(self, request, id=None, *args, **kwargs):
		
		product_object_list  = None
		category_object_list = None

		if id is not None:
			category_object_list, product_object_list = self.get_object()
			self.context['product_object_list']       = product_object_list
		else:
			category_object_list, product_object_list =self.get_object()
			self.context['product_object_list'] = product_object_list
			self.context['category_object_list'] = category_object_list
		return render(
            request,
            self.template_name,
            self.context
        )

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
				return get_success_url()
		# else:
		# 	form=ProductCreate()
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
				return redirect('Products:product-detail', id)
			# form=ProductCreate()
			
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
            return redirect("Products:product-list")
        return render(
            request,
            self.template_name,
            context,
        )
# <-------------- class based Product-Detail-Update-Delete view -------------->