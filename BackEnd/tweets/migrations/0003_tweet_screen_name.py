# Generated by Django 3.0.5 on 2020-12-27 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_auto_20201202_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='screen_name',
            field=models.TextField(default=''),
        ),
    ]