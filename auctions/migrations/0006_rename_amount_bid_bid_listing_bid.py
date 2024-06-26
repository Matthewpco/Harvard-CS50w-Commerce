# Generated by Django 4.2.4 on 2024-01-01 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_remove_user_bids_remove_user_listings_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='amount',
            new_name='bid',
        ),
        migrations.AddField(
            model_name='listing',
            name='bid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_bid', to='auctions.bid'),
        ),
    ]
