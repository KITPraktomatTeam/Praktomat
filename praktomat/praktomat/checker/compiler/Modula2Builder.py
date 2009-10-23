# $Id: Modula2Builder.py 901 2005-02-23 16:45:23Z stoerzer $
# -*- coding: iso-8859-1 -*-

# Copyright (C) 1999-2002 Universitaet Passau, Germany.
# Written by Andreas Zeller <zeller@acm.org>
# with extensions by Jens Krinke <j.krinke@gmx.de>
# and Maximilian Störzer <stoerzer@fmi.uni-passau.de>.
# 
# This file is part of Praktomat.
# 
# Praktomat is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
# 
# Praktomat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public
# License along with Praktomat -- see the file COPYING.
# If not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# 
# Praktomat is a programming course manager.
# For details, see the Praktomat WWW page, 
# `http://www.fmi.uni-passau.de/st/praktomat/',
# or send a mail to the Praktomat developers <praktomat@fmi.uni-passau.de>.

"""
Modula-2 Builder, using the Mocka compiler.
"""

import os
import re
import string

import Builder
import CheckerFactory

from misc import *

# Customize
MC       = "mc"
MC_FLAGS = "-range -index -static"
MC_LIBS  = ""

# Used commands
ECHO    = "echo"
DIRNAME = "dirname"
GREP    = "grep"
CUT     = "cut"

# A Modula-2 compiler for construction.
class Modula2Builder(Builder.Builder):

    #
    # Initialization sets own attributes to default values.
    #
    def __init__(self):
        Builder.Builder.__init__(self)
        # overwrite the settings
        self._compiler     = MC
        self._flags        = MC_FLAGS
        self._output_flags = "-o %s"
        self._libs         = MC_LIBS
        self._language     = "Modula-2"
        self._pattern      = "*.m?"
        self._rxarg        =  r"[a-zA-Z0-9_]*\.m."

    def result(self):
        return Modula2BuilderResult(self)

    # Create executable from sources
    def compile_command(self, env):
        # We use Mocka's `Lister' to get the annotated source printed
        # to standard output.  Unfortunately, Mocka is located in
        # different places on different hosts, so we must do a little
        # searching.

        program_name = env.program()

        cmd = ECHO + " 'p " + program_name + "' | (" + \
              "mockadir=`" + self.compiler() + " " + self.flags(env) + \
              " -info < /dev/null | " + \
              GREP + " List | " + CUT + " -d: -f2`; " + \
              "mockadir=`" + DIRNAME + " $mockadir`; " + \
              self.compiler() + " " + self.flags(env) + \
              " -list $mockadir/Lister )"

        return cmd

    def compile_command_invocation(self, env):
        return basename(self.compiler()) + " " + self.flags(env)

    # Include listing in output
    def enhance_output(self, env, output):
        program_name = env.program()
        
        # Make sure the commands appear in the log
        output = string.replace(output, ">> ",
                                ">> p " + program_name + "\n", 1)
        output = output[:string.rfind(output, ">> ")]

        # Mocka's listing output is called `LISTING'.
        listing = os.path.join(env.tmpdir(), 'LISTING')
        if os.path.isfile(listing):
            output = output + open(listing).read() + '\n'

        output = output + ">> q\n"

        return output


class Modula2BuilderResult(Builder.BuilderResult):
    
    # Stuff to highlight in output
    rxlisting  = re.compile(r"^@ LISTING.*$",        re.MULTILINE)
    rxlocation = re.compile(r"^@( *\^)$",            re.MULTILINE)
    rxerror    = re.compile(r"^@ *(.*)$",            re.MULTILINE)
    rxprompt   = re.compile(r"^&gt;&gt; (.*)$",      re.MULTILINE)


    def __init__(self, checker):
        BuilderResult.__init__(self, checker)

    # Enhanced output
    def htmlize_build_output(self, log):
        # Every line that starts with `@' is to be enhanced.        
        # Likewise, every line that starts with `>> '.
        hilite = r" <B><FONT COLOR=" + Checker.FAIL_COLOR + r"\1</FONT></B>"
        
        log = htmlize(log)
        log = re.sub(self.rxlisting, "", log)
        log = re.sub(self.rxlocation, hilite, log)
        log = re.sub(self.rxerror,    hilite, log)
        log = re.sub(self.rxwarning,  hilite, log)
        log = re.sub(self.rxprompt, r"&gt;&gt; <B>\1</B>", log)
        return log

#
# Register at the Checker factories.
#
CheckerFactory.checker_factory.register(Modula2Builder)
