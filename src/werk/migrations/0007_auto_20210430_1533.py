# Generated by Django 3.1.7 on 2021-04-30 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('werk', '0006_auto_20210430_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='werktask',
            name='end',
            field=models.DateTimeField(null=True),
        ),
    ]
