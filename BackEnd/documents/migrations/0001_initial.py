# Generated by Django 3.0.5 on 2020-11-01 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(default='')),
                ('raw_HTML', models.TextField(blank=True, default='')),
                ('text_body', models.TextField(blank=True, default='')),
                ('cleaned_tokens', models.TextField(blank=True, default='')),
            ],
        ),
    ]
