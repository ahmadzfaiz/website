# Generated by Django 4.1.5 on 2023-01-29 11:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+6281255555555'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('message', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='experience',
            name='image',
            field=models.ImageField(help_text='Rasio harus persegi. Contoh: 600px × 600px', upload_to='experience/'),
        ),
    ]
