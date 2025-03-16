from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from aliases.models import Alias
from aliases.tasks import sync_alias_to_mailgun


@receiver(post_save, sender=Alias)
def update_mailgun(sender, instance, created, **kwargs):
    transaction.on_commit(lambda: sync_alias_to_mailgun.delay(instance.id))
