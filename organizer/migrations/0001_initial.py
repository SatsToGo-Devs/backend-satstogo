# Generated by Django 5.0.3 on 2024-03-21 01:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('deadline', models.DateField()),
                ('event_type', models.CharField(choices=[(1, 'Admin'), (2, 'Staff'), (3, 'Customer')], max_length=10)),
                ('venue', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_business', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('parent_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizer.events')),
            ],
        ),
        migrations.AddField(
            model_name='events',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizer.organizer'),
        ),
    ]
