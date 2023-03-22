# Generated by Django 4.1.7 on 2023-03-22 07:01

import connection.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('connection_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('parameter', models.JSONField(default=dict)),
                ('is_deleted', models.BooleanField(blank=True, default=True, null=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Active'), (2, 'Inactive'), (3, 'Draft'), (4, 'New'), (5, 'Running'), (6, 'Pause'), (7, 'Stopped'), (8, 'Failed')], default=connection.models.StatusEnum['Active'], null=True)),
                ('created_by', models.IntegerField()),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'connection',
            },
        ),
        migrations.CreateModel(
            name='ConnectionType',
            fields=[
                ('connection_type_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('connection_type', models.CharField(max_length=300)),
                ('connection_type_name', models.CharField(max_length=300)),
                ('connection_type_code', models.CharField(max_length=300)),
                ('connection_type_description', models.CharField(max_length=500)),
                ('is_source_connection_type', models.BooleanField(blank=True, default=True, null=True)),
                ('is_destination_connection_type', models.BooleanField(blank=True, default=True, null=True)),
                ('application_code', models.CharField(max_length=300)),
                ('input_field_id', models.JSONField(default=dict)),
                ('output_field_id', models.JSONField(default=dict)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Active'), (2, 'Inactive'), (3, 'Draft'), (4, 'New'), (5, 'Running'), (6, 'Pause'), (7, 'Stopped'), (8, 'Failed')], default=connection.models.StatusEnum['Active'], null=True)),
                ('created_by', models.IntegerField()),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'connection_type',
            },
        ),
        migrations.CreateModel(
            name='FieldMaster',
            fields=[
                ('field_master_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('field_label', models.CharField(max_length=300)),
                ('field_type', models.CharField(max_length=300)),
                ('field_data_type', models.CharField(blank=True, max_length=300, null=True)),
                ('field_code', models.CharField(max_length=300)),
                ('backend_code', models.CharField(blank=True, max_length=300, null=True)),
                ('max_length', models.IntegerField(blank=True, default=100, null=True)),
                ('min_length', models.IntegerField(blank=True, default=1, null=True)),
                ('required', models.BooleanField(blank=True, default=True, null=True)),
                ('extras', models.JSONField(blank=True, default=dict, null=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Active'), (2, 'Inactive'), (3, 'Draft'), (4, 'New'), (5, 'Running'), (6, 'Pause'), (7, 'Stopped'), (8, 'Failed')], default=connection.models.StatusEnum['Active'], null=True)),
                ('created_by', models.IntegerField()),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'field_master',
            },
        ),
        migrations.CreateModel(
            name='ConnectionHistory',
            fields=[
                ('connection_history_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('changed_attributes', models.JSONField(blank=True, default=dict, null=True)),
                ('table_name', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('history_status', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.IntegerField()),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('connection_id', models.ForeignKey(db_column='connection_id', on_delete=django.db.models.deletion.CASCADE, to='connection.connection')),
            ],
            options={
                'db_table': 'connection_history',
            },
        ),
        migrations.AddField(
            model_name='connection',
            name='connection_type_id',
            field=models.ForeignKey(db_column='connection_type_id', on_delete=django.db.models.deletion.CASCADE, to='connection.connectiontype'),
        ),
    ]
