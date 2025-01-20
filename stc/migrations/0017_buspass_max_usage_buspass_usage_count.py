# Generated by Django 5.0.6 on 2024-11-28 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stc', '0016_buspass_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='buspass',
            name='max_usage',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='buspass',
            name='usage_count',
            field=models.IntegerField(default=0),
        ),
    ]
