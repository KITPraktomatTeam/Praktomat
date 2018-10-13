from django import template
from django.conf import settings

register = template.Library()

def do_get_motd(parser, token):
    # split_contents() knows not to split quoted strings.
    tokens = token.split_contents()
    if len(tokens) != 1:
        raise template.TemplateSyntaxError, "%r tag should have no arguments" % (tokens[0],)
    return MotdNode()

class MotdNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        if not settings.SYSADMIN_MOTD_URL:
            return ''
        return '<iframe src="%s" id="motd" onLoad="resize(\'motd\')" width="100%%"> </iframe>' % settings.SYSADMIN_MOTD_URL

register.tag('motd', do_get_motd)
