# Generated by Django 4.2 on 2023-06-23 06:45

from django.db import migrations, models
import hotplist.models


class Migration(migrations.Migration):

    dependencies = [
        ('hotplist', '0002_alter_hotplaces_rating_alter_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotplaces',
            name='origin_rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=2, validators=[hotplist.models.validate_rating]),
        ),
    ]
