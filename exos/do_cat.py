from task_builder import Task
import os


def install_basic_question():
    os.system('mkdir -p /.EFL /.EFL-verify /escape')
    os.system('touch /escape/where_am_i')

    txt = "+-----------------------------------------------------------------+\n"
    txt+= "| You are in the initial version of the EscapeFromLinux container |\n"
    txt+= "+-----------------------------------------------------------------+\n"

    f = open('/escape/where_am_i', 'w')
    f.write(txt)

    # how to detect a task is done
    os.system("mv /bin/ls  /.EFL/ls  && echo '#!/bin/bash\\necho 1 > /.EFL-verify/lsok \\n/.EFL/ls  $@' > /bin/ls  && chmod a+x /bin/ls")
    os.system("mv /bin/cat /.EFL/cat && echo '#!/bin/bash\\necho 1 > /.EFL-verify/catok\\n/.EFL/cat $@' > /bin/cat && chmod a+x /bin/cat")

def verify_file(filename):
    def verify_fct():
        try:
            if not os.path.exists(filename):
                return False, "do you realy find the binary to use ?"
            else:
                f = open(filename, "r")
                filecontent = f.read()
                if int(filecontent) == 1:
                    return True, "well done"
                else:
                    return False, "How did you do that ?!? maybe retry..."
        except:
            return True,f"Error while accessing verification file: {filename}, AUTOPASS QUESTION"
    return verify_fct



do_ls = Task(
        name="show directory content",
        description="use a binary to show the content of the /escape directory",
        clue="try 'ls' maybe ;)",
        value=1,
        install_function=install_basic_question,
        verify_function=verify_file( "/.EFL-verify/lsok" )
        )

do_cat = Task(
        name="show file content",
        description="use a binary to show the content of the /escape/where_am_i",
        clue="something like 'cat' ?",
        value=1,
        install_function=None,
        verify_function=verify_file( "/.EFL-verify/catok" ),
        parents=[ do_ls ]
        )

TASKS = [ do_ls, do_cat ]