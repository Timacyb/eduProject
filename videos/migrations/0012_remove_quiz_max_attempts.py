# Generated by Django 4.2 on 2025-01-12 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0011_quiz_max_attempts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='max_attempts',
        ),
    ]
