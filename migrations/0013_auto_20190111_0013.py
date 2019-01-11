# Generated by Django 2.1.3 on 2019-01-10 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battleships', '0012_auto_20190110_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete='cascade', related_name='winner', to='battleships.GamePlayer'),
        ),
    ]
