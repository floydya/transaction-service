# Generated by Django 3.0.6 on 2020-05-08 20:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('hook_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'account',
                'verbose_name_plural': 'accounts',
                'db_table': 'accounts',
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('type', models.CharField(choices=[('real', 'Real'), ('virtual', 'Virtual')], db_index=True, max_length=8)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallets', to='app.Account')),
            ],
            options={
                'verbose_name_plural': 'Wallets',
                'db_table': 'wallets',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('type', models.CharField(choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw'), ('canceled', 'Canceled')], max_length=8)),
                ('content_type_id', models.PositiveIntegerField()),
                ('entity_id', models.PositiveIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('description', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='app.Wallet')),
            ],
            options={
                'verbose_name_plural': 'Transactions',
                'db_table': 'transactions',
            },
        ),
    ]
