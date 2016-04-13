from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import escape
import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name,guess_lexer, guess_lexer_for_filename, ClassNotFound
from pygments.lexers._mapping import LEXERS

# This is a hack to register our Isabelle Lexer without patching pygments or using setuptools' entry_points.
LEXERS['IsarLexer'] = ('utilities.isar_lexer', 'Isabelle/Isar', ('isabelle',), ('*.thy',), ('text/x-isabelle',))

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
        return mark_safe("<pre>%s</pre>" % escape(value))


@register.filter(name='highlight_table')
@stringfilter
def colorize_table(value,arg=None):
    try:
        return mark_safe(highlight(value,get_lexer(value,arg),HtmlFormatter(linenos='table')))
    except ClassNotFound:
        return mark_safe("<pre>%s</pre>" % escape(value))

rx_diff_pm = re.compile('^(?P<first_line>\d*</pre></div></td><td class="code"><div class="highlight"><pre>)?(?P<line>(<span class=".*?">)?(?P<plusminus>\+|-).*?)(?P<endtag></pre>)?$')
rx_diff_questionmark = re.compile('(?P<line>(<span class="\w*">)?\?.*$)')
rx_tag = re.compile('^(<[^<]*>)+')
rx_char = re.compile('^(&\w+;|.)')
@register.filter
def highlight_diff(value):
	"enclose highlighted lines beginning with an +-? in a span"
	result = ""
	prevline = None
	for line in value.splitlines(1):
		m1 = rx_diff_questionmark.match(line)
		if m1:
			# We have a ? line. Instead of printing it, we annotate the previous line with the markers, which can be -, ^ or +
			# First remove newline from the end (or just all whitespace, does not hurt)
			line = line.rstrip()
			while line:
				# First strip all leading tags from both strings
				m2 = rx_tag.match(line)
				if m2:
					assert m2.end() > 0
					line = line[m2.end():]
					continue

				m2 = rx_tag.match(prevline)
				if m2:
					assert m2.end() > 0
					result += m2.group()
					prevline = prevline[m2.end():]
					continue

				# First character on both strings is a proper character
				cml = rx_char.match(line)
				assert cml, "regex rx_tag failed to match on non-empty string"
				cmpl = rx_char.match(prevline)
				if not cmpl:
					# This can only happen if the syntax highlighter changes the number of symbols (e.g. the Isabelle syntax highlighter)
					#assert cmpl, ("highlight_diff: previous line ended before ? marker. line: \"%s\", prevline: \"%s\"" % (line, prevline))
					line = line[cml.end():]
					continue

				lc = cml.group()
				plc = cmpl.group()

				if lc == '+':
					result += "<span class=\"addedChar\">%s</span>" % plc
				elif lc == '-':
					result += "<span class=\"deletedChar\">%s</span>" % plc
				elif lc == '^':
					result += "<span class=\"changedChar\">%s</span>" % plc
				elif lc == ' ' or lc == '?' or lc == '\t':
					result += plc
				else:
					assert False, ("Unexpected character in diff indicator line: \"%s\"" % lc)
					result += plc[0]
				line = line[cml.end():]
				prevline = prevline[cmpl.end():]
			result += prevline
			prevline = None
		else:
			if prevline is not None:
				result += prevline
			m = rx_diff_pm.match(line)
			if m:
				if m.group('first_line'):
					result += m.group('first_line')
				if m.group('plusminus') == '+':
					extra_class = "added"
				elif m.group('plusminus') == '-':
					extra_class = "removed"
				prevline = "<div class='changed %s'>%s</div>" % (extra_class, m.group('line'))
				if m.group('endtag'):
					prevline += m.group('endtag')
			else:
				prevline = line
	if prevline is not None:
		result += prevline
	return mark_safe(result)
