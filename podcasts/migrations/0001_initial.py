# Generated by Django 2.1.1 on 2018-11-02 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=200)),
                ('Summary', models.CharField(max_length=500)),
                ('Link', models.CharField(max_length=200)),
                ('PublishDate', models.DateTimeField(verbose_name='date published')),
                ('IsDownloaded', models.BooleanField(default=False)),
                ('DownloadResult', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
