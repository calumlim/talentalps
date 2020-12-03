# Generated by Django 3.1.3 on 2020-11-25 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_companyimage'),
        ('job', '0002_auto_20201123_0353'),
    ]

    operations = [
        migrations.AddField(
            model_name='joblisting',
            name='userprofile',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='user.userprofile', verbose_name='user profile'),
            preserve_default=False,
        ),
    ]
