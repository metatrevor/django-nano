from datetime import datetime

from django.template.loader import render_to_string

from nano.blog.models import Entry as _Entry

def add_entry_to_blog(object, headline, template, date_field=None):
    data = {'obj': object}
    template = render_to_string(template, dictionary=data)
    pub_date = object.__dict__.get(date_field or 'last_modified', datetime.now())
    blog_entry = _Entry.objects.create(content=template,headline=headline,pub_date=pub_date)

