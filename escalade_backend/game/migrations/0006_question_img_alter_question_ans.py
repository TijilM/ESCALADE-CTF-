# Generated by Django 4.0.2 on 2022-07-14 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_alter_question_link1_alter_question_link2'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='img',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='ans',
            field=models.CharField(max_length=500),
        ),
    ]
