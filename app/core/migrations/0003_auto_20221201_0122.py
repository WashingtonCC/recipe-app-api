# Generated by Django 3.2.16 on 2022-12-01 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='link',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]