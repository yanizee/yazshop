# Generated by Django 4.0.1 on 2022-05-17 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_beat_category_beat_file_beat_genre_beat_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beat',
            name='image',
            field=models.ImageField(upload_to='static/beats/img'),
        ),
        migrations.AlterField(
            model_name='pack',
            name='file',
            field=models.FileField(upload_to='static/packs'),
        ),
        migrations.AlterField(
            model_name='pack',
            name='image',
            field=models.ImageField(upload_to='static/packs/img'),
        ),
    ]