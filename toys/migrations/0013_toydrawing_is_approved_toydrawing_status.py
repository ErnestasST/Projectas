# Generated by Django 5.1.1 on 2024-09-17 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toys', '0012_toydrawing_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='toydrawing',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='toydrawing',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending Approval'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('rejected', 'Rejected')], default='pending', max_length=20),
        ),
    ]
