# Generated by Django 2.1.3 on 2019-01-06 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battleships', '0008_auto_20181220_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameplayer',
            name='game_nick',
            field=models.CharField(default='', max_length=200),
        ),
    ]
