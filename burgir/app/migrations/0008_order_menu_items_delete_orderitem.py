# Generated by Django 5.1.6 on 2025-02-07 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_order_menu_items_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='menu_items',
            field=models.ManyToManyField(related_name='orders', to='app.menuitem'),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
