# Generated by Django 4.0.2 on 2022-07-14 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0016_alter_team_level1_alter_team_level2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='is_loggedin',
            field=models.BooleanField(default=False),
        ),
    ]
