# Generated by Django 3.0.6 on 2020-09-29 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_auto_20200527_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='currency',
            field=models.CharField(choices=[(None, ''), ("so'm", "so'm"), ('$', 'dollor'), ('euro', 'euro'), ('ruble', 'ruble')], default='', max_length=5, verbose_name='Valyuta turi'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, help_text='Maxsulot haqida.', null=True, verbose_name='Tavfsifi'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Maxsulot Nomi'),
        ),
    ]
