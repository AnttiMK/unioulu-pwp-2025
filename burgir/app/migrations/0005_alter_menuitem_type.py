# Generated by Django 5.1.6 on 2025-02-07 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_menuitem_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='type',
            field=models.CharField(default='mainy ertr', max_length=20),
        ),
    ]
