# Generated by Django 3.2.4 on 2023-04-29 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20230429_0435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brochure',
            name='primary_color',
        ),
        migrations.RemoveField(
            model_name='brochure',
            name='secondary_color',
        ),
    ]