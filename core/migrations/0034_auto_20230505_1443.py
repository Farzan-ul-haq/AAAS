# Generated by Django 3.2.4 on 2023-05-05 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_product_show_on_landing'),
    ]

    operations = [
        migrations.AddField(
            model_name='dribbleproduct',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.CreateModel(
            name='PinterestProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('pinterest_id', models.CharField(blank=True, max_length=255, null=True)),
                ('redirect_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='market/pinterest/')),
                ('status', models.CharField(choices=[('P', 'PENDING'), ('A', 'APPROVED')], default='P', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.product')),
            ],
        ),
    ]
