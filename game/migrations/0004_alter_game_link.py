# Generated by Django 4.2 on 2024-02-25 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_alter_game_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='link',
            field=models.URLField(blank=True, null=True, unique=True),
        ),
    ]