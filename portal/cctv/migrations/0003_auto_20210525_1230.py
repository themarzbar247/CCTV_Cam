# Generated by Django 3.2.3 on 2021-05-25 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cctv', '0002_auto_20210523_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alerts',
            fields=[
                ('alertId', models.IntegerField(help_text='Unique ID for Alert', primary_key=True, serialize=False)),
                ('alertName', models.CharField(help_text='Name for the Alert', max_length=20)),
                ('alertDescription', models.TextField(help_text='Description of the specific alert ie what model was used', max_length=20)),
            ],
            options={
                'ordering': ['alertId'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notificationId', models.CharField(help_text='A unique alert notification ID', max_length=20, primary_key=True, serialize=False)),
                ('confidence', models.IntegerField(default=0, help_text='Confidence score given to the alert that fired')),
                ('firedDateTime', models.DateTimeField(help_text='Date Time that the alert was triggered')),
                ('sentDateTime', models.DateTimeField(auto_now=True, help_text='Date Time that the alert was sent')),
                ('description', models.CharField(help_text='description of the alert with metadata around triggered features', max_length=20)),
                ('alertContentLocation', models.CharField(help_text='a path to the content that trggered the alert for review', max_length=20)),
                ('alertId', models.ForeignKey(help_text='foreign key for the alert table', on_delete=django.db.models.deletion.RESTRICT, to='cctv.alerts')),
            ],
            options={
                'ordering': ['confidence', '-firedDateTime'],
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('typeId', models.IntegerField(help_text='Unique ID for Type', primary_key=True, serialize=False)),
                ('typeName', models.CharField(help_text='Name of the Alert type attribute', max_length=20)),
            ],
            options={
                'ordering': ['typeId'],
            },
        ),
        migrations.DeleteModel(
            name='Alert',
        ),
        migrations.AddField(
            model_name='alerts',
            name='typeId',
            field=models.ForeignKey(help_text='foreign key for the type table', on_delete=django.db.models.deletion.RESTRICT, to='cctv.type'),
        ),
    ]
