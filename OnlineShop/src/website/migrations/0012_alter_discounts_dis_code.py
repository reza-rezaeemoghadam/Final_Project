# Generated by Django 4.2 on 2024-09-03 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_alter_categories_options_alter_comments_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discounts',
            name='dis_code',
            field=models.UUIDField(unique=True),
        ),
    ]
