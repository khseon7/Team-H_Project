# Generated by Django 4.2 on 2023-06-24 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotplist', '0004_alter_hotplaces_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='wantlist',
            name='want_count',
            field=models.IntegerField(default=0),
        ),
    ]
