# Generated by Django 2.0.2 on 2018-03-06 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='text',
        ),
        migrations.AddField(
            model_name='challenge',
            name='additional_info',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='challengesourcetable',
            name='column_names_json',
            field=models.TextField(default='', editable=False),
        ),
        migrations.AlterField(
            model_name='challengesourcetable',
            name='content_rows_json',
            field=models.TextField(default='', editable=False),
        ),
    ]