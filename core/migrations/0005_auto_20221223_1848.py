# Generated by Django 3.2.7 on 2022-12-23 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20221121_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(choices=[('A', 'API'), ('L', 'Logo'), ('H', 'HTML TEMPLATE'), ('D', 'Software')], default='A', max_length=1)),
                ('name', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='MarketingPlatforms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('supported_products', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'Tag',
            },
        ),
        migrations.RenameField(
            model_name='apiservice',
            old_name='api_domain_url',
            new_name='base_url',
        ),
        migrations.RenameField(
            model_name='htmltemplate',
            old_name='download_file',
            new_name='source_file',
        ),
        migrations.RemoveField(
            model_name='downloadsoftware',
            name='download_file',
        ),
        migrations.RemoveField(
            model_name='logo',
            name='download_file',
        ),
        migrations.AddField(
            model_name='apiservice',
            name='in_scope',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='apiservice',
            name='out_scope',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='downloadsoftware',
            name='in_scope',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='downloadsoftware',
            name='out_scope',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='downloadsoftware',
            name='software_type',
            field=models.CharField(choices=[('OFFLINE', 'OFFLINE'), ('ONLINE', 'ONLINE')], default='ONLINE', max_length=100),
        ),
        migrations.AddField(
            model_name='downloadsoftware',
            name='source_file',
            field=models.FileField(null=True, upload_to='', verbose_name='software'),
        ),
        migrations.AddField(
            model_name='downloadsoftware',
            name='source_file_size',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='downloadsoftware',
            name='supported_os',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='htmltemplate',
            name='demo_site',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='htmltemplate',
            name='source_file_size',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='htmltemplate',
            name='supported_browser',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='logo',
            name='height',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='logo',
            name='logo_type',
            field=models.CharField(choices=[('PORTAIT', 'POTRAIT'), ('LANDSCAPE', 'LANDSCAPE'), ('SQUARE', 'SQUARE')], default='SQUARE', max_length=100),
        ),
        migrations.AddField(
            model_name='logo',
            name='source_file',
            field=models.FileField(default='', upload_to='', verbose_name='logo/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='logo',
            name='source_file_size',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='logo',
            name='width',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='source_url',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='apiservice',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='clientpackages',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='downloadsoftware',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='endpoints',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='htmltemplate',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='logo',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('A', 'API'), ('L', 'Logo'), ('H', 'HTML TEMPLATE'), ('D', 'Software')], default='A', max_length=1),
        ),
        migrations.AlterField(
            model_name='productpackage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'ADDED'), (1, 'SUBRACTED')], default=0)),
                ('coins', models.IntegerField(default=0)),
                ('content', models.CharField(default='', max_length=5000)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Transaction',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, to='core.Tag'),
        ),
    ]
