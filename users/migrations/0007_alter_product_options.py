# Generated by Django 5.1.1 on 2024-09-22 11:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_product_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "permissions": [
                    ("can_edit_product", "Can edit product"),
                    ("can_delete_product", "Can delete product"),
                ]
            },
        ),
    ]
