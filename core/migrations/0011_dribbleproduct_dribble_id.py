# Generated by Django 3.2.7 on 2023-01-12 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20230112_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='dribbleproduct',
            name='dribble_id',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
