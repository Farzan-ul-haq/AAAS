# Generated by Django 3.2.7 on 2023-01-11 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_dribbleproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='brochure',
            name='title',
            field=models.CharField(default='', max_length=5000),
        ),
    ]