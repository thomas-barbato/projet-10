# Generated by Django 3.2.18 on 2023-03-15 07:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0005_alter_users_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="user_id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False
            ),
        ),
    ]
