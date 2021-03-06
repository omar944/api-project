# Generated by Django 3.2.3 on 2021-08-09 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_text_post_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.DeleteModel(
            name='CourseRating',
        ),
        migrations.AddField(
            model_name='coursetime',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='times', to='api.course'),
        ),
    ]
