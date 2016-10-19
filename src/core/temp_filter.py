import json

from django.template import Library
register = Library()

@register.filter(is_safe=True)
def jsonfy(value):
    return json.dumps(value)

# register.filter('jsonfy',jsonfy)
# jsonfy.is_safe = True