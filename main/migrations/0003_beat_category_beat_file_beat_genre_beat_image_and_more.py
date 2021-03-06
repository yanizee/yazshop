# Generated by Django 4.0.1 on 2022-05-17 16:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_beat_options_alter_item_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='beat',
            name='category',
            field=models.CharField(default='Beat', max_length=10),
        ),
        migrations.AddField(
            model_name='beat',
            name='file',
            field=models.FileField(default='helpme', upload_to='static/img/beats'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='beat',
            name='genre',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='beat',
            name='image',
            field=models.ImageField(default='helpme2', upload_to='media/beats/img'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='beat',
            name='is_newest',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pack',
            name='category',
            field=models.CharField(default='Pack', max_length=10),
        ),
        migrations.AddField(
            model_name='pack',
            name='file',
            field=models.FileField(default='helpme3', upload_to='media/packs'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pack',
            name='image',
            field=models.ImageField(default='helpme4', upload_to='media/packs/img'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pack',
            name='is_newest',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='beat',
            name='bpm',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(200)]),
        ),
        migrations.AlterField(
            model_name='beat',
            name='key',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(blank=True, default=''),
        ),
    ]
