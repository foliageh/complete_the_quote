# Generated by Django 4.0 on 2022-08-16 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=150)),
                ('text', models.TextField(max_length=1000)),
                ('tags', models.TextField(max_length=500)),
                ('lang', models.CharField(default='en', max_length=7)),
            ],
        ),
    ]
