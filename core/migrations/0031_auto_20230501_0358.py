# Generated by Django 3.2.4 on 2023-05-01 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_product_review_average'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brochure',
            name='image',
        ),
        migrations.AddField(
            model_name='brochure',
            name='image_data',
            field=models.TextField(default=''),
        ),
    ]