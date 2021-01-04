# Generated by Django 3.0.5 on 2020-11-01 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.TextField(blank=False)),
                ('query', models.TextField(blank=False, default='')),
            ],),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.TextField(blank=False, default='')),
                ('created_at', models.DateTimeField()),
                ('text', models.TextField(blank=False, default='')),
                ('favorite_count', models.IntegerField(default=0)),
                ('retweet_count', models.IntegerField(default=0)),
                ('user_location', models.TextField(blank=False, default='')),
                ('sentiment', models.TextField(blank=False, default='')),
            ],
        ),
    ]
