# Generated by Django 4.2.8 on 2024-02-14 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wagers", "0003_remove_wagerparticipant_user_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="wagerparticipant",
            name="contributed_amount",
        ),
        migrations.RemoveField(
            model_name="wagerparticipant",
            name="winnings",
        ),
        migrations.AlterField(
            model_name="wager",
            name="creator",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="wagers_created",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="wager",
            name="participants",
            field=models.ManyToManyField(blank=True, related_name="wagers_participated", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name="wagerparticipant",
            name="participant",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="wagerparticipant",
            name="wager",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="wagers.wager"),
        ),
    ]
