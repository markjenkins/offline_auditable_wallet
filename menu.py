# Copyright Mark Jenkins, 2013
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

PROMPT_CHARACTERS = "> "

def always_return_false():
    return False

def run_breakable_menu(main_msg, prompt, options):
    pass

def run_menu(main_msg, prompt, options):
    print(main_msg)
    return options.get( input("%s %s" % (prompt, PROMPT_CHARACTERS)),
                        lambda : None )()
