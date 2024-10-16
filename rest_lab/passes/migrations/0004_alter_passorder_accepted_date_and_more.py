# Generated by Django 5.1.1 on 2024-10-16 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0003_passorder_moderator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passorder',
            name='accepted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='passorder',
            name='created_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='passorder',
            name='submited_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
