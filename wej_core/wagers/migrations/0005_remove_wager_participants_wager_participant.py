# Generated by Django 4.2.8 on 2024-02-14 17:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wagers", "0004_remove_wagerparticipant_contributed_amount_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="wager",
            name="participants",
        ),
        migrations.AddField(
            model_name="wager",
            name="participant",
            field=models.ManyToManyField(null=True, related_name="wagers_participated", to=settings.AUTH_USER_MODEL),
        ),
    ]
