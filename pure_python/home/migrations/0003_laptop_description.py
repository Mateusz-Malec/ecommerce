# Generated by Django 4.1.7 on 2023-03-18 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptop',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]