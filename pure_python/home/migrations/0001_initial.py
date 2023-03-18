# Generated by Django 4.1.7 on 2023-03-18 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(default='', max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(default='', max_length=15)),
                ('first_name', models.CharField(default='', max_length=30)),
                ('surname', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('product_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_fk', to='home.category')),
            ],
        ),
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.product')),
                ('name', models.CharField(max_length=150)),
                ('manufacturer', models.CharField(default='', max_length=20)),
                ('cpu', models.CharField(default='', max_length=50)),
                ('gpu', models.CharField(default='', max_length=50)),
                ('ram', models.CharField(default='', max_length=50)),
                ('system', models.CharField(default='', max_length=50)),
                ('image', models.ImageField(default='', upload_to='home/images')),
            ],
            bases=('home.product',),
        ),
        migrations.CreateModel(
            name='Desktop',
            fields=[
                ('computer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.computer')),
                ('description', models.TextField(blank=True)),
            ],
            bases=('home.computer',),
        ),
        migrations.CreateModel(
            name='Laptop',
            fields=[
                ('computer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.computer')),
                ('przekatna', models.DecimalField(decimal_places=1, default=15.5, max_digits=3)),
                ('disk', models.CharField(default='', max_length=50)),
            ],
            bases=('home.computer',),
        ),
    ]
