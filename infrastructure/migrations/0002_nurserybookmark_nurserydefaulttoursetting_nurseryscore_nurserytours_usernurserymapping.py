# Generated by Django 2.1.2 on 2018-11-10 13:36

from django.db import migrations, models
import django.utils.timezone
import django_mysql.models.fields.bit


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NurseryBookmark',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'nursery_bookmarks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NurseryDefaultTourSetting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('capacity', models.IntegerField()),
                ('description', models.CharField(max_length=255)),
                ('note', models.CharField(default=None, max_length=255)),
                ('is_active', django_mysql.models.fields.bit.Bit1BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'nursery_default_tour_settings',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NurseryScore',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.CharField(max_length=10)),
                ('score', models.IntegerField(default=None)),
                ('hierarchy', models.CharField(max_length=255)),
                ('note', models.CharField(max_length=255)),
                ('is_active', django_mysql.models.fields.bit.Bit1BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'nursery_scores',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NurseryTours',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('special_start_time', models.TimeField(default=None)),
                ('special_end_time', models.TimeField(default=None)),
                ('special_capacity', models.TimeField(default=None)),
                ('special_note', models.CharField(default=None, max_length=255)),
                ('is_active', django_mysql.models.fields.bit.Bit1BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'nursery_tours',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserNurseryMapping',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', django_mysql.models.fields.bit.Bit1BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'user_nursery_mappings',
                'managed': False,
            },
        ),
    ]
