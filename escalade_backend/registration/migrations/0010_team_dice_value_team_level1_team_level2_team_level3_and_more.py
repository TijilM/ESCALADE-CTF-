# Generated by Django 4.0.2 on 2022-07-06 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
        ('registration', '0009_remove_participant_current_ques_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='dice_value',
            field=models.SmallIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='level1',
            field=models.CharField(default='0102030405060708091011121314151617181920', max_length=50),
        ),
        migrations.AddField(
            model_name='team',
            name='level2',
            field=models.CharField(default='2122232425262728293031323334353637383940', max_length=50),
        ),
        migrations.AddField(
            model_name='team',
            name='level3',
            field=models.CharField(default='4142434445464748495051525354555657585960', max_length=50),
        ),
        migrations.AddField(
            model_name='team',
            name='level4',
            field=models.CharField(default='6162636465666768697071727374757677787980', max_length=50),
        ),
        migrations.AlterField(
            model_name='team',
            name='current_ques',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.question'),
        ),
    ]
