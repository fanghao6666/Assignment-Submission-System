# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-10 07:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('year', models.IntegerField(choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')], default=1)),
                ('roll_no', models.CharField(max_length=8, unique=True)),
                ('created', models.DateField(editable=False, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='student_id',
        ),
        migrations.AddField(
            model_name='assignment',
            name='created',
            field=models.DateField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='updated',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='solution',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='deadline',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='year',
            field=models.IntegerField(choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')], default=1),
        ),
        migrations.AlterField(
            model_name='solution',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
