# Generated by Django 4.0.1 on 2022-05-17 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_beat_image_alter_pack_file_alter_pack_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beat',
            name='file',
            field=models.FileField(upload_to='static/beats'),
        ),
    ]
