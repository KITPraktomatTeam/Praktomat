# -*- coding: utf-8 -*-

"""
A C compiler for construction.
"""

from django.conf import settings
from checker.compiler.Builder import Linker
from checker.compiler.Builder import IncludeHelper
from checker.compiler.Builder import LibraryHelper
from checker.compiler.Builder import MainNeedHelper

import os, re
from utilities.safeexec import execute_arglist

from django.utils.translation import ugettext_lazy as _


class CLinker(Linker, LibraryHelper, MainNeedHelper):
    """ A C compiler for construction. """

    # Initialization sets attributes to default values.
    _linker            = settings.C_BINARY
    _OBJECTINSPECTOR    = "findMainInObject" # shell script name in folder scripts calling nm
    _OBJINSPECT_PAR        = "nm -A -C".split(" ")
    _language        = "C"
    #_rx_warnings        = r"^([^ :]*:[^:].*)$"


    def main_search(self,env):
        """ returns module name if main is found in object file """
        main_symbol = "main"
        #output of nm -A -C  mytest.o is: mytest.o:0000000d T main
        nm_rx  = re.compile(r"^(.*/)*(.*)\.[oO]:[0-9A-Fa-f]* T (main)$", re.MULTILINE)
        obj_files = []
        c_rx = re.compile('^(.*\.)[cC]')
        #ToDo: code review
        o_solution_list = [re.sub(r"\.[cC]",r".o",name)\
            for (name,void) in env.sources()\
            if name.endswith(('.c','.C'))]

        for dirpath, dirs, files in os.walk(env.tmpdir()):
            for filename in files:
                if filename.endswith(('.O', '.o')):
                        #ToDo: code review
                    #if object file corresponds to a student uploaded solution file
                    if filename in o_solution_list:
                        obj_files.append(filename)
                        # Next let's shell out and search in object file for main
                        script_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'scripts')
                        cmd = [os.path.join(script_dir, self._OBJECTINSPECTOR)] + self._OBJINSPECT_PAR + [os.path.join(dirpath,filename)]
                        [objinfo,error,exitcode,timed_out,oom_ed]  = execute_arglist(cmd , env.tmpdir(), self.environment(), timeout=settings.TEST_TIMEOUT, fileseeklimit=settings.TEST_MAXFILESIZE, extradirs=[script_dir])
                        if exitcode != 0 :
                            raise self.NotFoundError("Internal Server Error. Processing files %s" % ",".join(obj_files)+"\n"+objinfo)
                        tmp = re.search(nm_rx, objinfo)
                        if tmp and len(tmp.groups(2)):
                            self.main_object_name = re.search(nm_rx,objinfo).group(2)
                            self.main_object_name = tmp.group(2)
                            return self.main_object_name

        raise self.NotFoundError("An object containing the main symbol (i.e. 'int main(int argc, char* argv[])' ) could not be found in the files %s" % ", ".join(obj_files))


# todo: code review
    def main_module(self,env):
        try:
            return self.main_object_name if self.main_object_name else self.main_search(env)
        except AttributeError:
            return self.main_search(env)


    def get_file_names(self,env):

        # Get all object files corresponding to solutions C files.
        c_rx = re.compile('^(.*\.)[cC]')
        o_solution_list = [re.sub(r"\.[cC]", r".o", name)\
            for (name,void) in env.sources()\
            if name.endswith(('.c','.C'))]


        #ToDo: rethink if object files should add to env here - perhaps not! ...
        # add these object files to env sources
        for f in o_solution_list:
            try:
                for (name, void) in env.sources():
                     if f == name: raise StopIteration
                     env.add_source(f, None)
            except StopIteration: pass

        #rxarg = re.compile(self.rxarg())
        #return [name for (name,content) in env.sources() if rxarg.match(name)]
        return super(CLinker,self).get_file_names(env)

    def logbuilder(self,output,args,env):
        return self.build_log(output,args,self.get_file_names(env))


    def pre_run(self,env):
        return self.linker()



    def post_run(self,env):
        passed = True
        log = ""
        try:
            self.main_module(env)

        except self.NotFoundError as e:
            log +=  str(e)
            # But only complain if the main method is required
            if self.main_required():
                log = "Error: " + log
                passed = False
            else:
                passed = True
                log = "Info: " + log

        return [passed,log]


    def connected_flags(self, env):
        return self.flags() + self.search_path() + self.libs()




from checker.admin import CheckerInline, AlwaysChangedModelForm

class CheckerForm(AlwaysChangedModelForm):

    """ override default values for the model fields """
    def __init__(self, **args):
        super(CheckerForm, self).__init__(**args)
        self.fields["_flags"].initial = "-Wl,--warn-common"
        #self.fields["_output_flags"].initial = "-o %s"
        #self.fields["_output_flags"].default = "-o %s"
        #self.fields["_output_flags"].choices = _LINK_CHOICES
        #self.fields["_output_flags"].help_text = _('\'%s\' will be replaced by the output name.')
        self.fields["_libs"].initial = ""
        self.fields["_file_pattern"].initial = r"^[a-zA-Z0-9_]*\.[oO]$"
        #self.fields["_main_required"].label = _("link as executable program")
        #self.fields["_main_required"].help_text = _("if not activated, object files code will be compiled to object file *.o! Compiler uses -c option")



class CLinkerInline(CheckerInline):
    model = CLinker
    form = CheckerForm
    verbose_name = "C Linker"


