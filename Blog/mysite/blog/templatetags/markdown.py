from django import template
import markdown

register = template.Library()


@register.filter
def markdown_format(text):
    return markdown.markdown(text)