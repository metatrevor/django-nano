from django.db import models

class Entry(models.Model):
    headline = models.CharField(max_length=255)
    content = models.TextField()
    pub_date = models.DateTimeField()

    class Meta:
        db_table = 'nano_blog_entry'
        verbose_name_plural = 'entries'

    def __unicode__(self):
        return self.headline
