# Generated manually to match packages/models.py changes:
# - tour_type choices updated ("College Tour" -> "Friends Tour",
#   "Weekend Tour" -> "Weekend Getaway")
# - added starting_price, popular_destinations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='tour_type',
            field=models.CharField(choices=[('Family Tour', 'Family Tour'), ('Corporate Tour', 'Corporate Tour'), ('Temple Tour', 'Temple Tour'), ('Friends Tour', 'Friends Tour'), ('Weekend Getaway', 'Weekend Getaway'), ('Honeymoon Tour', 'Honeymoon Tour')], max_length=30),
        ),
        migrations.AddField(
            model_name='package',
            name='starting_price',
            field=models.CharField(blank=True, help_text="e.g. \u20b94,999 per person \u2014 shown as a 'starting from' price on the card", max_length=50),
        ),
        migrations.AddField(
            model_name='package',
            name='popular_destinations',
            field=models.CharField(blank=True, help_text='Comma-separated, e.g. Kerala, Ooty, Munnar', max_length=300),
        ),
    ]
