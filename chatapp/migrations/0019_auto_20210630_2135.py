# Generated by Django 3.1.7 on 2021-06-30 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0018_auto_20210630_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagegroup',
            name='content',
            field=models.CharField(max_length=10000),
        ),
    ]
