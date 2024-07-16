# Generated by Django 5.0.7 on 2024-07-16 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_train_arrival_time_train_date_train_departure_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='section',
            field=models.CharField(choices=[('Sleeper', 'Sleeper'), ('Upper Berth', 'Upper Berth'), ('Lower Berth', 'Lower Berth'), ('AC Coach', 'AC Coach')], default='Sleeper', max_length=20),
        ),
        migrations.AddField(
            model_name='train',
            name='sections',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='train',
            name='schedule',
            field=models.CharField(choices=[('Daily', 'Daily'), ('Every two days', 'Every two days')], default='Daily', max_length=20),
        ),
    ]