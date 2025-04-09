from django import template

register=template.Library()

@register.filter
def get_list(dict,key):
    return dict.get(key,[])