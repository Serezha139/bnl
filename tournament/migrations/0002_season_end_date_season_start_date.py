# Generated by Django 4.2 on 2024-05-07 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='season',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
