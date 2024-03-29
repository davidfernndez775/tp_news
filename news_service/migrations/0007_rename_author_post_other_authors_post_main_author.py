# Generated by Django 4.2.7 on 2024-02-03 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news_service', '0006_remove_journalist_journalist_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='author',
            new_name='other_authors',
        ),
        migrations.AddField(
            model_name='post',
            name='main_author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='main_author', to='news_service.journalist'),
            preserve_default=False,
        ),
    ]
