# Generated by Django 5.1.1 on 2024-10-13 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0002_passorder_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='passorder',
            name='moderator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='m_orders', to='passes.authuser'),
        ),
    ]
