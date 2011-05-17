from datetime import datetime

from django.conf import settings
from django.db import models

from nano.tools import get_user_model
from nano.tools.models import UnorderedTreeMixin, GenericForeignKeyAbstractModel

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH',3000)

User = get_user_model() 

class Comment(GenericForeignKeyAbstractModel, UnorderedTreeMixin):
    user = models.ForeignKey(User,
            blank=True, null=True, related_name="%(class)s_comments") 
    comment = models.TextField(max_length=COMMENT_MAX_LENGTH)
    comment_xhtml = models.TextField(editable=False)
    added = models.DateTimeField(default=datetime.utcnow)
    is_visible = models.BooleanField(default=True)
    is_scrambled = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = "nano_comments_comment"
        ordering = ('added',)
        get_latest_by = 'added'

    def __unicode__(self):
        return "%s: %s..." % (self.user, self.comment[:49]+'...' if len(self.comment) > 50 else self.comment)    
        
    def get_content_object_url(self):
        return self.content_object.get_absolute_url() or ''

    def get_absolute_url(self, anchor_pattern="#c%(id)s"):
        content_url = self.get_content_object_url()
        anchor = anchor_pattern % self.__dict__
        if content_url:
            return content_url + anchor
        return anchor

