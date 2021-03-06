# Generated by Django 2.1.3 on 2018-12-02 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battleships', '0002_auto_20181202_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrier',
            name='game_player',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='battleships.GamePlayer'),
        ),
        migrations.AlterField(
            model_name='destroyer',
            name='game_player',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='battleships.GamePlayer'),
        ),
        migrations.AlterField(
            model_name='frigate',
            name='game_player',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='battleships.GamePlayer'),
        ),
        migrations.AlterField(
            model_name='submarine',
            name='game_player',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='battleships.GamePlayer'),
        ),
    ]
