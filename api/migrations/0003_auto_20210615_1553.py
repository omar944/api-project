# Generated by Django 3.2.3 on 2021-06-15 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_api', '0002_auto_20210615_1553'),
        ('api', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='user_api.user')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='api.post')),
            ],
        ),
    ]
