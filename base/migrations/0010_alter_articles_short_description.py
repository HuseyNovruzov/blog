# Generated by Django 4.0.5 on 2022-07-20 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_articles_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='short_description',
            field=models.TextField(max_length=250, null=True),
        ),
    ]