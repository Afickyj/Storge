# Generated by Django 5.1.1 on 2024-09-22 14:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_order_orderitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="address",
            field=models.CharField(default="Neznámá adresa", max_length=255),
        ),
        migrations.AddField(
            model_name="order",
            name="delivery_method",
            field=models.CharField(
                choices=[("courier", "Kurýr"), ("pickup", "Osobní odběr")],
                default="courier",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("cash", "Hotově při doručení"),
                    ("card", "Kartou při doručení"),
                ],
                default="cash",
                max_length=10,
            ),
        ),
    ]
