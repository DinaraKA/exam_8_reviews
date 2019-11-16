# Generated by Django 2.2 on 2019-11-16 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Product')),
                ('category', models.CharField(choices=[('other', 'Other'), ('book', 'Book'), ('hotel', 'Hotel'), ('car', 'Car')], default='other', max_length=50, verbose_name='Category')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images', verbose_name='Image')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]