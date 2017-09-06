from django import template
from django.utils.safestring import mark_safe

import markdown2


register = template.Library() 

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