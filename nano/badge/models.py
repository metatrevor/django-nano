from django.db import models

from nano.tools import get_user_model, get_profile_model

User = get_user_model()

class DefaultManager(models.Manager):
    pass

class Badge(models.Model):
    """
    Three fields:
        level - integer, default: 100
        name - text, max. 20 chars
        description - text, aim for one line

    receivers -> User.badges
    """
    level = models.PositiveIntegerField(default=100)
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    receivers = models.ManyToManyField(User, blank=True, null=True, related_name='badges')

    class Meta:
        db_table = 'nano_badge_badge'

    def __unicode__(self):
        return self.name

