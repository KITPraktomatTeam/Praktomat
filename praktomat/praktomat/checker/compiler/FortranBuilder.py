# $Id: FortranBuilder.py 901 2005-02-23 16:45:23Z stoerzer $
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
A FORTRAN compiler for construction.
"""

import Builder
import CheckerFactory

F77       = "g77"
F77_FLAGS = "-Wall -static"
F77_LIBS  = ""

# A FORTRAN compiler for construction.
class FortranBuilder(Builder.Builder):

        #
    # Initialization sets own attributes to default values.
    #
    def __init__(self):
        Builder.Builder.__init__(self)
        # overwrite the settings
        self._compiler     = F77
        self._flags        = F77_FLAGS
        self._output_flags = "-o %s"
        self._libs         = F77_LIBS
        self._language     = "FORTRAN 77"
        self._pattern      = "*.f"
        self._rxarg        = r"[a-zA-Z0-9_]*\.(f|F|for|FOR)"

#
# Register at the Checker factories.
#
CheckerFactory.checker_factory.register(FortranBuilder)
