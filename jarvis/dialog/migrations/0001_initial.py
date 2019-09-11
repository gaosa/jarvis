# Generated by Django 2.2.5 on 2019-09-11 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_type', models.CharField(choices=[('Q', 'Question'), ('A', 'User Command'), ('G', 'Graph Json')], max_length=1)),
                ('content', models.TextField()),
                ('dialog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dialog.Dialog')),
            ],
        ),
    ]