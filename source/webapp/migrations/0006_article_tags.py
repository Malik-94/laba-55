# Generated by Django 2.2.6 on 2019-10-15 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='articles', to='webapp.Tag', verbose_name='Теги'),
        ),
    ]
