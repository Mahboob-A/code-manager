# Generated by Django 4.2.11 on 2024-05-29 07:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("code_display", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="companies",
            name="title",
            field=models.CharField(max_length=255, verbose_name="Company Title"),
        ),
    ]
