"""
Mixin-models, with minimal example implementations.

"""

from datetime import datetime

from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.db import models
from django.utils.translation import ugettext_lazy as _

from nano.tools import get_user_model
User = get_user_model()

class UnorderedTreeMixin(models.Model):
    part_of = models.ForeignKey('self', blank=True, null=True, default=None)
    path = models.CharField(max_length=255, blank=True, default='')

    _sep = u'/'

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            super(UnorderedTreeMixin, self).save(*args, **kwargs)

        self._set_path()
        super(UnorderedTreeMixin, self).save(*args, **kwargs)


    def _set_path(self):

        if self.part_of:
            self.path = "%s%i/" % (self.part_of.path, self.id)
        else:
            self.path = "%i/" % self.id

    @property
    def level(self):
        return unicode(self.path).count(self._sep)

    def roots(self):
        return self._default_manager.filter(part_of__isnull=True)

    def get_path(self):
        return [self._default_manager.get(id=p) for p in unicode(self.path).split(self._sep)]

    def descendants(self):
        return self._default_manager.filter(path__startswith=self.path).exclude(id=self.id)

    def parent(self):
        return self.part_of

    def siblings(self):
        return [p for p in self.part_of.descendants() if p.level == self.level]

    def children(self):
        return [p for p in self.descendants() if p.level == self.level + 1]

    def is_sibling_of(self, node):
        return self.part_of == node.part_of

    def is_child_of(self, node):
        return self.part_of == node

    def is_root(self):
        """Roots have no parents"""

        return bool(self.part_of)

    def is_leaf(self):
        """Leaves have no descendants"""

        return self.descendants().count() == 0

class PathField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(PathField, self).__init__(*args, **kwargs)

    def db_type(self):
        return 'text'

class PathMixin(models.Model):
    path = models.TextField()

    class Meta:
        abstract = True

    def save(self, parent=None, *args, **kwargs):
        if not parent:
            self.path = str(self.id) + '/'
#         else:
#             parentpath = 
        
        super(PathMixin, self).save(*args, **kwargs)

    def is_ancestor(self, obj):
        if self.path.startswith(obj.path):
            return True
        return False

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

# class ShunList(AbstractShunList):
# 
#     class Meta:
#         db_table = 'nano_tools_shunlist'
# 
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

class GenericForeignKeyAbstractModel(models.Model):
    """
    An abstract base class for models with one GenericForeignKey
    """

    # Content-object field
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'), related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    class Meta:
        abstract = True
