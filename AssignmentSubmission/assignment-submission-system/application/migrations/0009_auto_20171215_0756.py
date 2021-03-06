# Generated by Django 2.0 on 2017-12-14 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_auto_20171215_0739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(default='', on_delete=True, to='application.Course'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='teacher',
            field=models.ForeignKey(default='', on_delete=True, to='application.UserProfile'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='assignment',
            field=models.ForeignKey(on_delete=True, to='application.Assignment'),
        ),
    ]
