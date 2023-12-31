# Generated by Django 4.2.3 on 2023-08-10 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonds', '0002_alter_images_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deals',
            options={'ordering': ['time_create', 'custom_time'], 'verbose_name_plural': 'Deals'},
        ),
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name_plural': 'Ratings'},
        ),
        migrations.AddField(
            model_name='deals',
            name='custom_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deals',
            name='price_at_the_time',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
    ]
