# Generated by Django 4.1.7 on 2023-03-22 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rule_engine', '0003_commonmaster_cm_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tblrulesconfiguration',
            name='rules_id',
        ),
        migrations.AddField(
            model_name='tblrulesconfiguration',
            name='rules_set_id',
            field=models.ForeignKey(db_column='rules_set_id', default=1, on_delete=django.db.models.deletion.CASCADE, to='rule_engine.tblrulesset'),
            preserve_default=False,
        ),
    ]
