# Generated by Django 3.1.4 on 2020-12-29 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0003_tweet_screen_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='screen_name',
            field=models.TextField(blank=True, default=''),
        ),
    ]
