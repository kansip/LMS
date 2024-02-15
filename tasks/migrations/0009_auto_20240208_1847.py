# Generated by Django 3.2.24 on 2024-02-08 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_task_number_of_attempts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='integer_format_flag',
        ),
        migrations.AddField(
            model_name='task',
            name='file_format_flag',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='task',
            name='text_format_flag',
            field=models.BooleanField(default=1),
        ),
    ]