# Generated by Django 3.2.18 on 2023-03-28 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_author_user_id_projects_author_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment_id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
    ]