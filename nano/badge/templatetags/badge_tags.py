from django import template
from django.core.urlresolvers import reverse

from nano.badge.models import Badge

register = template.Library()

SYMBOLS = {
    100: u'\u26ab',
    200: u'\u26ab',
    300: u'\u26ab',
}

SYMBOL_NAMES = {
    100: 'bronze',
    200: 'silver',
    300: 'gold',
}

def sum_badges(profile):
    levels = {}
    for badge in profile.badges.all():
        levels[badge.level] = levels.setdefault(badge.level, 0) + 1

    return levels

@register.simple_tag
def show_badges(user):
    profile = user.get_profile()
    inner_template = u'<span class="b%i" title="%s %s badge%s">%s</span>%i'
    outer_template = u'<span>%s</span>'

    levels = sum_badges(profile)

    sorted_levels = reversed(sorted(levels.keys()))
    out = []
    for level in sorted_levels:
        name = SYMBOL_NAMES[level]
        symbol = SYMBOLS[level]
        num_levels = levels[level]
        plural = u's' if num_levels > 1 else u''
        out.append(inner_template % (level, num_levels, name, plural, symbol, num_levels))

    return outer_template % u' '.join(out)

@register.simple_tag
def show_badge(badge):
    template = u'<span class="badge"><a href="%(link)s"><span class="b%(level)i" >%(symbol)s</span> %(name)s</a></span>'
    fillin = {
        'level': badge.level,
        'symbol': SYMBOLS[badge.level],
        'name': badge.name,
        'link': reverse('badge-detail', args=[badge.id]),
    }
    return template % fillin

@register.simple_tag
def show_badge_and_freq(badge):
    template = u'<span class="badge-freq">%s (%i)</span>'
    badge_text = show_badge(badge)
    return template % (badge_text, badge.receivers.count())
