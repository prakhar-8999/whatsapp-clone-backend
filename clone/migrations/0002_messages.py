# Generated by Django 2.2 on 2022-09-19 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clone', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('sender', models.IntegerField()),
                ('receiver', models.IntegerField()),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]