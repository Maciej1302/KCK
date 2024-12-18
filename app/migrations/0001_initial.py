# Generated by Django 5.1.2 on 2024-11-10 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50, verbose_name='Brand')),
                ('model', models.CharField(max_length=50, verbose_name='Model')),
                ('first_registration', models.DateField(verbose_name='First Registration')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('color', models.CharField(max_length=30, verbose_name='Color')),
                ('engine_capacity', models.PositiveIntegerField(verbose_name='Engine Capacity (cc)')),
                ('power', models.PositiveIntegerField(verbose_name='Power (HP)')),
            ],
            options={
                'verbose_name': 'Car',
                'verbose_name_plural': 'Cars',
            },
        ),
    ]
