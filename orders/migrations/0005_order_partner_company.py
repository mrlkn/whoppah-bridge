# Generated by Django 5.1.6 on 2025-03-20 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_order_weight_class_order_weight_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='partner_company',
            field=models.CharField(blank=True, choices=[('HOEKSTRA', 'Hoekstra'), ('VINTAGE_EXPRESS', 'Vintage Express'), ('MAGIC_MOVERS', 'Magic Movers'), ('SW_DE_VRIES_LOGISTICS', 'SW de Vries Logistics'), ('LIBERO_LOGISTICS', 'Libero Logistics'), ('TRANSPOKSI', 'Transpoksi'), ('TRUSK', 'Trusk'), ('COCOLIS', 'Cocolis'), ('MH_TRANSPORT', 'MH Transport')], max_length=50, null=True, verbose_name='Partner Company'),
        ),
    ]
