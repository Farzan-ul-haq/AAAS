# Generated by Django 3.2.4 on 2023-05-04 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_clientactivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='show_on_landing',
            field=models.BooleanField(default=False),
        ),
    ]