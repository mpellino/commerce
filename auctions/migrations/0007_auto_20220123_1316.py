# Generated by Django 3.2.9 on 2022-01-23 13:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_comments_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bid', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bid',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bid',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bid', to='auctions.auctionlisting'),
        ),
        migrations.AddField(
            model_name='bid',
            name='value',
            field=models.PositiveIntegerField(default=None),
        ),
    ]
