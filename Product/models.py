from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Category(models.Model):
    name=models.CharField(
        max_length=250,
        unique=True,
        verbose_name='Kategoriya Nomi',
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
class Product(models.Model):    
	name=models.CharField(
        max_length=50,
        verbose_name='Maxsulot Nomi',
    )
	category=models.ForeignKey(
        "Category", 
        verbose_name='Maxsulot Kategoriyasi',
        related_name='product_name', 
        on_delete=models.CASCADE
    )
	description=models.TextField(
        blank=True, 
        null=True,
        verbose_name='Tavfsifi',
    )
	image=models.ImageField(
        upload_to='images', 
        height_field=None, 
        width_field=None, 
        max_length=255,
        verbose_name='Maxsulot Rasmi',
        blank=True, 
        null=True
    )

    #Choice class for currency 
	class CurrecyChoice(models.TextChoices):
		SUM="so\'m",_('so\'m')
		USD='$',_('dollor')
		EUR='euro',_('euro')
		RUB='ruble',_('ruble')
		__empty__=_('')
	currency=models.CharField(
        max_length=5,
        choices=CurrecyChoice.choices,
        default=CurrecyChoice.__empty__,
        verbose_name='valyuta turi'
    )
	price=models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Maxsulot Narxi',
		default=100,
		validators=(
            MinValueValidator(100),
            MaxValueValidator(100000000),
        )
    )
	published_at=models.DateTimeField(
        auto_now_add=True
    )
	updated_at=models.DateTimeField(
        auto_now=True
    )

	class Meta:
		verbose_name = 'Product'
		verbose_name_plural = 'Products'
    
	def __str__(self):
		return self.name
    
	def get_absolute_url(self):
		return reverse("Product:product-detail", kwargs={"id": self.id})

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		print('URL:', url)
		return url

	def get_absolute_url(self):
		return reverse("Product:product-detail", kwargs={"id": self.id})

    
class ProductImage(models.Model):
	product=models.ForeignKey(Product, on_delete=models.CASCADE)
	short_caption=models.CharField(
        max_length=250, 
        blank=True, 
        null=True
    )
	image=models.ImageField(
        upload_to='images', 
        height_field=None, 
        width_field=None, 
        max_length=250,
        blank=True,
        null=True,
    )

	def __str__(self):
		return self.short_caption
    
	@property
	def imageURL(self):
		try:
			url=self.image.url
		except:
			url=''
		return url

