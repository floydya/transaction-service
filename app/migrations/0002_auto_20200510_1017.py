# Generated by Django 3.0.6 on 2020-05-10 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='content_type_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='entity_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw'), ('zero', 'Zero'), ('canceled', 'Canceled')], max_length=8),
        ),
    ]