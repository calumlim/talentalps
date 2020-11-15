# Generated by Django 3.1.3 on 2020-11-15 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_auto_20201025_2322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joblisting',
            name='qualifications',
        ),
        migrations.RemoveField(
            model_name='joblisting',
            name='specialisation',
        ),
        migrations.AddField(
            model_name='joblisting',
            name='job_functions',
            field=models.CharField(choices=[('it', 'Information Technology'), ('engineering', 'Engineering')], default='it', max_length=80, verbose_name='job functions'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='joblisting',
            name='industry',
            field=models.CharField(choices=[('it_services', 'Information Technology & Services'), ('telecommunications', 'Telecommunications')], max_length=80, verbose_name='industry'),
        ),
    ]
