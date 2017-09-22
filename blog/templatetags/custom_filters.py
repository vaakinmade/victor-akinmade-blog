from django import template
from django.utils.safestring import mark_safe
from dateutil.relativedelta import relativedelta
import datetime
import markdown2


register = template.Library()

@register.filter('date_format')
def date_format(date):
	years_ago = datetime.datetime.now() - relativedelta(years=5)
	return years_ago

@register.filter('time_estimate')
def time_estimate(word_count):
    '''Estimates the number of minutes it will take to read a post
    based on the passed-in wordcount.
    '''
    minutes = round(word_count/450)
    return minutes


@register.filter('markdown_to_html')
def markdown_to_html(markdown_text):
    '''Converts markdown text to HTML'''
    html_body = markdown2.markdown(markdown_text, extras=["fenced-code-blocks",])
    return mark_safe(html_body)


@register.filter('add_int')
def add_int(x, y):
    """
    Adds the x and y and returns as floating points
    """
    return int(x) + int(y)