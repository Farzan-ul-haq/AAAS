# Generated by Django 3.2.7 on 2023-01-22 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20230120_1111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brochuretemplates',
            old_name='template_text',
            new_name='template_html_text',
        ),
        migrations.AddField(
            model_name='brochuretemplates',
            name='template_js_text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
