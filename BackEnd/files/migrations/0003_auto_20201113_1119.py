# Generated by Django 3.0.5 on 2020-11-13 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_auto_20201113_0930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='content',
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='input_files'),
        ),
    ]