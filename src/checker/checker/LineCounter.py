# -*- coding: utf-8 -*-

"""
Generate some simple lexical statistics.
"""

import string

from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.basemodels import Checker

class LineCounter(Checker):
    """ Lexical Statistics of the sources.
        This class is not really a checker, as it only gathers some simple
        lexical statistics of the source code:
        - number of files
        - lines, lines of code and lines of comment """

    def title(self):
        """ Returns the title for this checker category. """
        # _de("Lexikalische Statistik")
        return ugettext("Lexical statistics")

    @staticmethod
    def description():
        """ Returns a description for this Checker. """
        # _de(u"Diese Prüfung wird immer bestanden.")
        return ugettext("This check is always passed.")

    def run(self, env):
        """ Here's the actual work.     This runs the check in the environment ENV,
        returning a CheckerResult. """

        log = ""
        passed = 1

        files = 0
        lines = 0
        comment_lines = 0
        code_lines = 0
        coco_lines = 0

        in_long_comment = 0

        # Here's how to access the sources.
        for (name, content) in env.string_sources():
            assert not in_long_comment
            in_short_comment = 0

            files = files + 1

            lines_in_file = 0
            comment_lines_in_file = 0
            code_lines_in_file = 0
            coco_lines_in_file = 0

            line_has_comment = 0
            line_has_code = 0

            for i in range(len(content)):
                # sets both lookaheads (if available)
                la1 = content[i]
                la2 = '\0'
                if i+1 < len(content):
                    la2 = content[i+1]

                if la1 == '\n':
                    # new line
                    lines_in_file = lines_in_file + 1
                    if line_has_comment:
                        comment_lines_in_file = comment_lines_in_file + 1
                    if line_has_code:
                        code_lines_in_file = code_lines_in_file + 1
                    if line_has_comment and line_has_code:
                        coco_lines_in_file = coco_lines_in_file + 1

                    line_has_comment = 0
                    line_has_code = 0
                    in_short_comment = 0
                    continue

                if in_long_comment and la1 == '*' and la2 == "/":
                    in_long_comment = 0
                    continue

                if in_long_comment or in_short_comment:
                    if    la1 in string.digits or la1 in string.ascii_letters:
                        line_has_comment = 1
                else:
                    if la1 in string.digits or la1 in string.ascii_letters:
                        line_has_code = 1
                    if la1 == "/":
                        if la2 == "*":
                            in_long_comment = 1
                            continue
                        if la2 == "/":
                            in_short_comment = 1
                            continue

            try:
                # FIXME : code_lines_in_file, comment_lines_in_file
                #          may be 0!!
                # _de()
                # log = log + (    escape(name) + ": "
                #              + `lines_in_file` + " Zeilen, davon "
                #              + `code_lines_in_file` + " Code ("
                #              + `code_lines_in_file*100 / lines_in_file` + "%), "
                #              + `comment_lines_in_file` + " Kommentar ("
                #              + `comment_lines_in_file*100 / lines_in_file` + "%), "
                #              + `coco_lines_in_file` + " beides ("
                #              + `coco_lines_in_file*100 / lines_in_file` + "%).<br>\n")
                l = ugettext(
                    "{0} lines, including {1} code lines ({2}%), {3} comment lines ({4}%), {5} both ({6}%)."
                    .format(lines_in_file,
                        code_lines_in_file,
                        code_lines_in_file*100 / lines_in_file,
                        comment_lines_in_file,
                        comment_lines_in_file*100 / lines_in_file,
                        coco_lines_in_file,
                        coco_lines_in_file*100 / lines_in_file))
                log = log + (    escape(name) + ": " + l + "<br>\n")

            except ZeroDivisionError:
                # FIXME
                log = log + "Line Width Checker (l 178): ZeroDivisionError " + \
                      " (no comment / code / coco lines in file!)"

            lines = lines + lines_in_file
            comment_lines = comment_lines + comment_lines_in_file
            code_lines = code_lines + code_lines_in_file
            coco_lines = coco_lines + coco_lines_in_file

        # All files have been processed.
        try:
            # _de()
            # log = log + ("<br>" + `files` + " Dateien, "
            #              + `lines` + " Zeilen, davon "
            #              + `code_lines` + " Code ("
            #              + `code_lines * 100 / lines` + "%), "
            #              + `comment_lines` + " Kommentar ("
            #              + `comment_lines * 100 / lines` + "%), "
            #              + `coco_lines` + " beides ("
            #              + `coco_lines * 100 / lines` + "%).\n")
            l = ugettext(
                "{0} files, {1} lines, including {2} code lines ({3}%), {4} comment lines ({5}%), {6} both ({7}%)."
                .format(files,
                    lines,
                    code_lines,
                    code_lines * 100 / lines,
                    comment_lines,
                    comment_lines * 100 / lines,
                    coco_lines,
                    coco_lines * 100 / lines)
                )
            log = log + ("<br>" + l + "\n")

        except ZeroDivisionError:
            # FIXME
            log = log + "Line Width Checker (l 197): ZeroDivisionError " + \
                  " (no comment / code / coco lines in file!)"

        # Generate the result.
        result = self.create_result(env)
        result.set_log(log)
        result.set_passed(passed)
        # That's all!
        return result

from checker.admin import CheckerInline
class LineCounterInline(CheckerInline):
    model = LineCounter
