# Generated by Django 3.1.2 on 2020-10-24 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_auto_20201024_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='joblisting',
            name='expired',
            field=models.BooleanField(default=False, verbose_name='expired'),
        ),
        migrations.AddField(
            model_name='joblisting',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='views'),
            preserve_default=False,
        ),
    ]
