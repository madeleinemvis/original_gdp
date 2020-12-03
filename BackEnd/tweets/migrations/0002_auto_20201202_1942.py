# Generated by Django 3.0.5 on 2020-12-02 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='sentiment',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='uid',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='user_location',
            field=models.TextField(blank=True, default=''),
        ),
    ]