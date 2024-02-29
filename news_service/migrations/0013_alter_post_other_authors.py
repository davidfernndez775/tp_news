# Generated by Django 4.2.7 on 2024-02-26 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_service', '0012_remove_journalist_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='other_authors',
            field=models.ManyToManyField(blank=True, null=True, through='news_service.JournalistPost', to='news_service.journalist'),
        ),
    ]