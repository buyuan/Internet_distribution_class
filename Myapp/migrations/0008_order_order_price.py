# Generated by Django 4.0.5 on 2022-07-08 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0007_rename_stage_course_stages'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]