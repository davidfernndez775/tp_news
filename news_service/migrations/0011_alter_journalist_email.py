# Generated by Django 4.2.7 on 2024-02-14 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_service', '0010_journalist_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalist',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
