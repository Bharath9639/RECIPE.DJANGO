# Generated by Django 4.2.5 on 2023-09-23 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='recipe_img',
            field=models.ImageField(upload_to='images'),
        ),
    ]
