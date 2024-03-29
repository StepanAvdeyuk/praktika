# Generated by Django 3.1.3 on 2020-11-21 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scopedata',
            old_name='enable_bool',
            new_name='check_enable',
        ),
        migrations.RenameField(
            model_name='scopedata',
            old_name='filter_bool',
            new_name='check_filter',
        ),
        migrations.RenameField(
            model_name='scopedata',
            old_name='invert_bool',
            new_name='check_invert',
        ),
        migrations.AddField(
            model_name='scopedata',
            name='average',
            field=models.CharField(choices=[(' ', ' '), ('4', '4'), ('16', '16'), ('64', '64'), ('128', '128'), ('256', '256')], default=' ', max_length=12, verbose_name='average'),
        ),
        migrations.AlterField(
            model_name='scopedata',
            name='ch_coupling',
            field=models.CharField(choices=[('DC', 'DC'), ('AC', 'AC'), ('GND', 'GND')], default='DC', max_length=3, verbose_name='ch_coupling'),
        ),
        migrations.AlterField(
            model_name='scopedata',
            name='ch_probe',
            field=models.CharField(choices=[('1', '1'), ('10', '10'), ('100', '100'), ('1000', '1000')], default='1', max_length=4, verbose_name='ch_probe'),
        ),
        migrations.AlterField(
            model_name='scopedata',
            name='ch_scale',
            field=models.CharField(choices=[('10.0V/div', '10.0V/div'), ('5.00V/div', '5.00V/div'), ('2.00V/div', '2.00V/div'), ('1.00V/div', '1.00V/div'), ('500mV/div', '500mV/div')], default='10.0V/div', max_length=12, verbose_name='ch_scale'),
        ),
        migrations.AlterField(
            model_name='scopedata',
            name='fetch_mode',
            field=models.CharField(choices=[('Sampling', 'Sampling'), ('Pulse', 'Pulse'), ('Video', 'Video'), ('Slope', 'Slope'), ('Alter', 'Alter')], default='Sampling', max_length=8, verbose_name='fetch_mode'),
        ),
        migrations.AlterField(
            model_name='scopedata',
            name='insert',
            field=models.CharField(choices=[('Sine', 'Sine'), ('Line', 'Line')], default='Sine', max_length=4, verbose_name='insert'),
        ),
        migrations.AlterField(
            model_name='scopedata',
            name='trig_mode',
            field=models.CharField(choices=[('Auto', 'Auto'), ('Normal', 'Normal'), ('Single', 'Single')], default='Auto', max_length=6, verbose_name='trig_mode'),
        ),
        migrations.AlterField(
            model_name='scopedata',
            name='trig_source',
            field=models.CharField(choices=[('CH1', 'CH1'), ('CH2', 'CH2'), ('EXT', 'EXT'), ('EXT/5', 'EXT/5'), ('AC Line', 'AC Line')], default='CH1', max_length=7, verbose_name='trig_source'),
        ),
        migrations.AlterField(
            model_name='scopedata',
            name='trig_type',
            field=models.CharField(choices=[('Edge', 'Edge'), ('Pulse', 'Pulse'), ('Video', 'Video'), ('Slope', 'Slope'), ('Alter', 'Alter')], default='Edge', max_length=5, verbose_name='trig_type'),
        ),
    ]
