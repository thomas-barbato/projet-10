# Generated by Django 3.2.18 on 2023-03-14 16:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="user",
            field=models.PositiveIntegerField(
                editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
