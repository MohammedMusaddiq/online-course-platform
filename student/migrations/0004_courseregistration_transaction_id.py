# Generated by Django 4.0.5 on 2022-07-05 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_courseregistration_paid_delete_courseorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseregistration',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
