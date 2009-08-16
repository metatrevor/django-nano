from django.db import models

from nano.tools import get_user_model, get_profile_model

Profile = get_profile_model()

class DefaultManager(models.Manager):
    pass

class Badge(models.Model):
    level = models.PositiveIntegerField(default=100)
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    receivers = models.ManyToManyField(Profile, blank=True, null=True, related_name='badges')

    class Meta:
        db_table = 'nano_badge_badge'

    def __unicode__(self):
        return self.name

