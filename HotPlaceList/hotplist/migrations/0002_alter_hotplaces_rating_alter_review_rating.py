# Generated by Django 4.2 on 2023-06-14 08:03

from django.db import migrations, models
import hotplist.models


class Migration(migrations.Migration):

    dependencies = [
        ('hotplist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotplaces',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=2, validators=[hotplist.models.validate_rating]),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=2, validators=[hotplist.models.validate_rating]),
        ),
    ]