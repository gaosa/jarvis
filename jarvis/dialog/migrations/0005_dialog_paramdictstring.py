# Generated by Django 2.2.5 on 2019-10-05 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0004_remove_dialog_graphjsonstring'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialog',
            name='paramDictString',
            field=models.TextField(default='{}'),
        ),
    ]
