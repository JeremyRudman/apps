# Generated by Django 4.2.13 on 2025-02-11 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campaigns", "0018_campaign_call_to_action_header"),
    ]

    operations = [
        migrations.AddField(
            model_name="campaign",
            name="donation_goal_show_numbers",
            field=models.BooleanField(default=True),
        ),
    ]
