from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode

from nano import comments
from nano.comments.models import * 

register = template.Library()

@register.inclusion_tag('nano/comments/comment_list_frag.html')
def show_comments(object):
    contenttype = ContentType.objects.get_for_model(object)
    comments = Comment.objects.filter(object_pk=str(object.id), content_type=contenttype)
    return {'comments': comments}

@register.inclusion_tag('nano/comments/comment_tree_frag.html')
def show_comments_tree(object):
    contenttype = ContentType.objects.get_for_model(object)
    comments = Comment.tree.roots().filter(object_pk=str(object.id), content_type=contenttype)
    return {'comments': comments}

@register.inclusion_tag('nano/comments/comment_tree_node_frag.html')
def show_comments_subtree(subtree):
    comments = subtree.children()
    return {'comments': comments}
