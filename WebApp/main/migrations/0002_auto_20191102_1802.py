# Generated by Django 2.2.6 on 2019-11-02 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='is_training',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='image',
            name='is_fire',
            field=models.IntegerField(default=0),
        ),
    ]
