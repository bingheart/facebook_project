# Generated by Django 4.0 on 2024-03-14 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0004_alter_users_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='posts_url',
            field=models.CharField(default=1, max_length=250, verbose_name='post_url'),
            preserve_default=False,
        ),
    ]
