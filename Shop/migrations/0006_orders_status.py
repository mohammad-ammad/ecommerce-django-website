# Generated by Django 3.1.7 on 2021-03-23 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0005_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]