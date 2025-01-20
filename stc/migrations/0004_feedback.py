# Generated by Django 5.1 on 2024-10-01 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stc', '0003_rto_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_text', models.TextField()),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
