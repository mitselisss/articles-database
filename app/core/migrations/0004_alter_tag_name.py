# Generated by Django 3.2.25 on 2025-06-12 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20250612_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(default='Tag name to be added', max_length=255, unique=True),
        ),
    ]
