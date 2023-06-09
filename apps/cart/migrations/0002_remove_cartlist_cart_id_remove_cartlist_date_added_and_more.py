# Generated by Django 4.2.1 on 2023-05-10 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_categories_options_alter_fruits_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartlist',
            name='cart_id',
        ),
        migrations.RemoveField(
            model_name='cartlist',
            name='date_added',
        ),
        migrations.AddField(
            model_name='cartlist',
            name='fruit',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='shop.fruits'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartlist',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='cartlist',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Products',
        ),
    ]
