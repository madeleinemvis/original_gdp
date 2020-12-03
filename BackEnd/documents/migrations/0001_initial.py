# Generated by Django 3.0.5 on 2020-11-01 19:56
import jsonfield
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]


operations = [
    migrations.CreateModel(
        name='Claim',
        fields=[
            ('uid', models.TextField(blank=False)),
            ('claim', models.TextField(blank=False, default='')),
        ]
    ),
    migrations.CreateModel(
        name='Document',
        fields=[
            ('uid', models.TextField(blank=False)),
            ('content_type', models.TextField(blank=False, default='')),
            ('url', models.TextField(default='')),
            ('raw_html', models.TextField(blank=True, default='')),
            ('title', models.TextField(blank=True, default='')),
            ('text_body', models.TextField(blank=True, default='')),
            ('cleaned_tokens', jsonfield.fields.JSONField()),
            ('html_links', jsonfield.fields.JSONField()),
        ],
    ),
]
