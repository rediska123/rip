# Generated by Django 5.1.1 on 2024-10-13 17:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='passorder',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to='passes.authuser'),
        ),
    ]
