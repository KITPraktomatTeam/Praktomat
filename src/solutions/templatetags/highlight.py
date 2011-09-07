from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name,guess_lexer, guess_lexer_for_filename, ClassNotFound

register = template.Library()

def get_lexer(value,arg):
    if arg is None:
        return guess_lexer(value)
    return guess_lexer_for_filename(arg,value) #get_lexer_by_name(arg)

@register.filter(name='highlight')
@stringfilter
def colorize(value, arg=None):
    try:
        return mark_safe(highlight(value,get_lexer(value,arg),HtmlFormatter()))
    except ClassNotFound:
        return value


@register.filter(name='highlight_table')
@stringfilter
def colorize_table(value,arg=None):
    try:
        return mark_safe(highlight(value,get_lexer(value,arg),HtmlFormatter(linenos='table')))
    except ClassNotFound:
        return value

rx_diff = re.compile('^(?P<first_line>\d*</pre></div></td><td class="code"><div class="highlight"><pre>)?(?P<line>(<span class=".*?">)?(\+|-|\?).*$)')     
@register.filter
def highlight_diff(value):
	"enclose highlighted lines beginning with an +-? in a span"
	result = ""
	for line in value.splitlines(1):
		m = rx_diff.match(line)
		if m:
			result += (m.group('first_line') or "") + "<div class='changed'>" + m.group('line') + "</div>"
		else:
			result += line
	return mark_safe(result)
