# Generated by Django 5.0.4 on 2024-04-18 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangesettlement',
            name='settlement_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]