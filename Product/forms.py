from django import forms

from .models import (Product, Category)


# <-------------- Creation Product -------------->
class CategoryCreate(forms.ModelForm):
	name=forms.CharField(
		max_length=250, 
		required=True,
		widget=forms.TextInput(
			attrs={
				'placeholder' : 'Enter Category name'
			}
		)	
	)
	class Meta:
		model=Category
		fields=(
			'name',
		)
# <-------------- Creation Product -------------->


# <-------------- Creation Product -------------->
class ProductCreate(forms.ModelForm):
	class Meta:
		model=Product
		fields=(
			'category',
			'name',
			'description',
			'image',
			'currency',
			'price',

		)

# <-------------- Creation Product -------------->