# Generated by Django 5.0.2 on 2024-11-28 05:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stc', '0009_user_from_address_user_to_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=4, max_digits=300)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('wuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.user')),
            ],
        ),
    ]
