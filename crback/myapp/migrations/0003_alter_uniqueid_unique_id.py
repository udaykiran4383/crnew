# Generated by Django 5.0.7 on 2024-07-27 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_userprofile_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uniqueid',
            name='unique_id',
            field=models.CharField(max_length=50),
        ),
    ]
