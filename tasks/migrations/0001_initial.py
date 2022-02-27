# Generated by Django 3.2.7 on 2022-02-27 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('desc', models.TextField()),
                ('cost', models.IntegerField()),
                ('category', models.CharField(max_length=20)),
                ('revizion_format_flag', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TaskFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.FileField(upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='TaskTrueAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('true_flags', models.TextField()),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('local', models.IntegerField()),
                ('data_open', models.DateTimeField()),
                ('data_part_close', models.DateTimeField()),
                ('data_close', models.DateTimeField()),
                ('open', models.BooleanField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('tasks', models.ManyToManyField(to='tasks.Task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('time', models.DateTimeField()),
                ('score', models.IntegerField()),
                ('revizion', models.BooleanField(default=0)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='files',
            field=models.ManyToManyField(to='tasks.TaskFiles'),
        ),
    ]
