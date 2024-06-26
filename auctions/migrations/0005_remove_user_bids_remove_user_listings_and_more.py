# Generated by Django 4.2.4 on 2023-12-31 23:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_bid_listing_bid_user_comments_listing_comments_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bids',
        ),
        migrations.RemoveField(
            model_name='user',
            name='listings',
        ),
        migrations.AddField(
            model_name='comments',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.RemoveField(
            model_name='bid',
            name='user',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='user',
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Bid_Users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Comment_Users', to=settings.AUTH_USER_MODEL),
        ),
    ]
