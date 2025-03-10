# Generated by Django 5.0.2 on 2024-11-28 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stc', '0012_busroute'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusConductor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
                ('busname', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
