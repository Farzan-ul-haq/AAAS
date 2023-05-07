# Generated by Django 3.2.4 on 2023-05-07 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_coroloftproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('A', 'approved'), ('R', 'rejected'), ('P', 'pending'), ('D', 'deleted')], default='D', max_length=1),
        ),
    ]
