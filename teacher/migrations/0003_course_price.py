# Generated by Django 4.0.5 on 2022-07-04 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_rename_name_course_course_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]