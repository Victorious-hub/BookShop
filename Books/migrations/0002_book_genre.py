# Generated by Django 4.1.6 on 2023-06-28 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('Fantasy', 'Fantasy'), ('Adventure', 'Adventure'), ('Love', 'Love'), ('Historic', 'Historic'), ('Detective', 'Detective')], max_length=255, null=True),
        ),
    ]