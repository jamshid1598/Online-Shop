from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Category(models.Model):
    name = models.CharField( verbose_name='Kategoriya Nomi', max_length=250, unique=True, )
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
class Product(models.Model):    
	name        = models.CharField( verbose_name='Maxsulot Nomi', max_length=250, )
	category    = models.ForeignKey( "Category", 
                verbose_name = 'Maxsulot Kategoriyasi',
                related_name = 'product_name', 
                on_delete    = models.CASCADE
            )
	description = models.TextField( verbose_name='Tavfsifi', help_text="Maxsulot haqida.", blank=True, null=True, )
	image       = models.ImageField( #default image
                upload_to='images', 
                max_length=255,
                verbose_name='Maxsulot Rasmi',
                blank=True, 
                null=True
            )

    # Class for choosing currency type 
	class CurrecyChoice(models.TextChoices):
		SUM="so\'m",_('so\'m')
		USD='$',_('dollor')
		EUR='euro',_('euro')
		RUB='ruble',_('ruble')
		__empty__=_('')
	currency    = models.CharField( verbose_name='Valyuta turi', max_length=5,
                choices=CurrecyChoice.choices,
                default=CurrecyChoice.__empty__,
            )
	price       = models.DecimalField( verbose_name='Maxsulot Narxi', max_digits=10, decimal_places=2, default=100,
                validators=(
                    MinValueValidator(100),
                    MaxValueValidator(100000000),
                )
            )
	published_at = models.DateTimeField( auto_now_add=True )
	updated_at  =models.DateTimeField( auto_now=True )

	class Meta:
		verbose_name = 'Product'
		verbose_name_plural = 'Products'
    
	def __str__(self):
		return self.name
    
	def get_absolute_url(self):
		return reverse("Products:product-detail", kwargs={"id": self.id})

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		print('URL:', url)
		return url
    
class ProductImage(models.Model):
	product       = models.ForeignKey(Product, on_delete=models.CASCADE)
	short_caption = models.CharField( max_length=250, blank=True, null=True )
	image         = models.ImageField(
                  upload_to    = 'images', 
                  height_field = None, 
                  width_field  = None, 
                  max_length   = 250,
                  blank        = True,
                  null         = True,
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

