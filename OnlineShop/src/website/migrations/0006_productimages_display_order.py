# Generated by Django 4.2 on 2024-08-14 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_alter_comments_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimages',
            name='display_order',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
