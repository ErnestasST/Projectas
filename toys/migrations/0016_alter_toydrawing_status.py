# Generated by Django 5.1.1 on 2024-09-19 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toys', '0015_toydrawing_user_alter_toydrawing_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toydrawing',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
