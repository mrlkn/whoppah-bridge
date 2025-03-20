# Generated by Django 5.1.6 on 2025-03-20 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_dropoffaddress_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='weight_class',
        ),
        migrations.AddField(
            model_name='order',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='weight'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('canceled', 'Canceled'), ('accepted', 'Accepted'), ('shipped', 'Shipped'), ('disputed', 'Disputed'), ('completed', 'Completed'), ('expired', 'Expired'), ('delivered', 'Delivered')], default='new', max_length=20, verbose_name='Order Status'),
        ),
    ]
