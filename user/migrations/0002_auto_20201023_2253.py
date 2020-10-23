# Generated by Django 3.1.2 on 2020-10-23 14:53

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='header',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.get_avatar_image_path, verbose_name='avatar'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='header',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.get_header_image_path, verbose_name='header'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='verified'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='description',
            field=models.TextField(blank=True, max_length=1200, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='company',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.get_company_avatar_image_path, verbose_name='avatar'),
        ),
        migrations.AlterField(
            model_name='company',
            name='header_image',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.get_company_header_image_path, verbose_name='header image'),
        ),
    ]