# Generated by Django 2.0 on 2017-12-14 07:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_auto_20171112_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
