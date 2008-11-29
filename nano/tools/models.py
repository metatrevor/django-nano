"""
Mixin-models, with minimal example implementations.

"""

from datetime import datetime

from django.db import models
from django.conf import settings

from nano.tools import get_user_model
User = get_user_model()

class AbstractShunList(models.Model):
    """AbstractShunList
        User x shuns User y: one of:
         - ``ShunList.objects.create(user=x, shuns=y)``
         - ``x.shuns.add(y)``
         - ``y.shunned_by.add(x)``

    """
    
    user = models.ForeignKey(User, related_name='%(class)s_shuns')
    shuns = models.ForeignKey(User, related_name='%(class)s_shunned_by')

    class Meta:
        abstract = True

class ShunList(AbstractShunList):

    class Meta:
        db_table = 'nano_tools_shunlist'

class AbstractText(models.Model):
    "Denormalized storage of text"
    DEFAULT_TYPE = 'plaintext'
    text = models.TextField()
    text_formatted = models.TextField(editable=False)
    text_type = models.CharField(max_length=64, default=DEFAULT_TYPE)

    class Meta:
        abstract = True

    def save(self, formatters=None, *args, **kwargs):
        if self.text_type == self.DEFAULT_TYPE:
            self.text_formatted = self.text
        else:
            if formatters:
                self.text_formatted = formatters(self.text_type)
        super(AbstractText, self).save(*args, **kwargs)
