# Generated by Django 4.2.3 on 2023-07-12 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonds',
            name='g_spread',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='bonds',
            name='z_spread',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
