# Generated by Django 5.1.2 on 2024-10-29 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stc', '0004_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
