# Generated by Django 3.0.6 on 2020-05-13 08:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200510_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='hook_url',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
