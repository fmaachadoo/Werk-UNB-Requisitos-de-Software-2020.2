# Generated by Django 3.1.7 on 2021-04-30 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('werk', '0007_auto_20210430_1533'),
    ]

    operations = [
        migrations.RenameField(
            model_name='werktask',
            old_name='end',
            new_name='end_time',
        ),
        migrations.AddField(
            model_name='werktask',
            name='total_time',
            field=models.TimeField(null=True),
        ),
    ]