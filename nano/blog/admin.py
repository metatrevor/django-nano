
from django.contrib import admin

from nano.blog.models import *

class EntryAdmin(admin.ModelAdmin):
    model = Entry
    list_display = ('headline', 'pub_date')

admin.site.register(Entry, EntryAdmin)
