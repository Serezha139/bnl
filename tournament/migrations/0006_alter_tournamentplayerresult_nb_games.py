# Generated by Django 4.2 on 2023-05-01 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0005_rename_tournamentplayerresults_tournamentplayerresult_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentplayerresult',
            name='nb_games',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
