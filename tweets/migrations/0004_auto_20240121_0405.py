# Generated by Django 3.1.3 on 2024-01-21 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0003_tweetphoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='comments_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='tweet',
            name='likes_count',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
