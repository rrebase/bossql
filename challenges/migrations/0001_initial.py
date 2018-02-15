# Generated by Django 2.0.2 on 2018-02-15 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('challenge_id', models.IntegerField(primary_key=True, serialize=False)),
                ('challenge_name', models.CharField(max_length=200)),
                ('challenge_desc', models.TextField()),
                ('challenge_text', models.TextField()),
                ('challenge_available', models.BooleanField(default=True)),
            ],
        ),
    ]
