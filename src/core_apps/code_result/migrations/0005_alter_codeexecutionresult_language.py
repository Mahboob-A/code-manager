# Generated by Django 4.2.11 on 2024-05-01 09:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("code_result", "0004_alter_codeexecutionresult_language"),
    ]

    operations = [
        migrations.AlterField(
            model_name="codeexecutionresult",
            name="language",
            field=models.CharField(
                choices=[("py", "Python"), ("cpp", "C++"), ("java", "Java")],
                default="py",
                max_length=25,
                verbose_name="Programming Language",
            ),
        ),
    ]
