# Generated by Django 5.2 on 2025-04-10 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wishlist", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="card",
            name="exclusive",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
