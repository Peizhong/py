# Generated by Django 2.0.5 on 2018-07-08 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_auto_20180706_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='subs_name',
            field=models.CharField(default='null', max_length=100),
            preserve_default=False,
        ),
    ]
