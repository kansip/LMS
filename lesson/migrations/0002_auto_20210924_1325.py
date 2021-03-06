# Generated by Django 3.2.7 on 2021-09-24 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_alter_course_image'),
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='date',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='teacher',
        ),
        migrations.AddField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='course.course'),
            preserve_default=False,
        ),
    ]
