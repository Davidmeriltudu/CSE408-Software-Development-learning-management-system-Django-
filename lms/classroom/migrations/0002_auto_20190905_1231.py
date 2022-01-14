# Generated by Django 2.2.1 on 2019-09-05 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classroom', '0001_initial'),
        ('signUp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signUp.Course'),
        ),
        migrations.AddField(
            model_name='resource',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signUp.Teacher'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signUp.Course'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signUp.Teacher'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.Quiz'),
        ),
        migrations.AddField(
            model_name='marks',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.Quiz'),
        ),
        migrations.AddField(
            model_name='marks',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signUp.Student'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signUp.Course'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='discussionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.DiscussionId'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='signUp.Student'),
        ),
        migrations.AddField(
            model_name='discussion',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='signUp.Teacher'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.Question'),
        ),
    ]
