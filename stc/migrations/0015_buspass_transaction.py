# Generated by Django 5.0.6 on 2024-11-28 14:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stc', '0014_busconductor_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusPass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_address', models.CharField(max_length=255)),
                ('to_address', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='bus_pass_qr/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.user')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('bus_pass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.buspass')),
                ('conductor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stc.busconductor')),
            ],
        ),
    ]
