# Generated by Django 4.2.11 on 2024-05-01 09:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("code_result", "0003_codeexecutionresult_language"),
    ]

    operations = [
        migrations.AlterField(
            model_name="codeexecutionresult",
            name="language",
            field=models.CharField(
                default="py", max_length=25, verbose_name="Programming Language"
            ),
        ),
    ]
