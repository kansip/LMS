# Generated by Django 3.2.24 on 2024-02-09 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_auto_20240209_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskanswers',
            name='files',
            field=models.FileField(default=None, upload_to='uploads'),
        ),
    ]