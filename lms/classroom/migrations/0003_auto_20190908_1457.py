# Generated by Django 2.2.1 on 2019-09-08 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0002_auto_20190905_1231'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='last_date',
            new_name='exam_date',
        ),
        migrations.AddField(
            model_name='quiz',
            name='start_time',
            field=models.TimeField(default=None, verbose_name='start time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quiz',
            name='time',
            field=models.CharField(max_length=200),
        ),
    ]