# Generated by Django 4.0.5 on 2022-06-30 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0006_course_interested_course_stage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='stage',
            new_name='stages',
        ),
    ]
