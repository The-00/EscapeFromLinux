from task_builder import Task
import os


def install_basic_question():
    os.system('mkdir -p /.EFL /.EFL-verify /escape')
    os.system('touch /escape/where_am_i')

    txt = "+-----------------------------------------------------------------+\n"
    txt+= "| New Tasks :                                                     |\n"
    txt+= "|   1: install wget and validate the task (debian system)         |\n"
    txt+= "|   2: install caca-utils (yes it's a real package for caca lib   |\n"
    txt+= "|                                            img manipulation lib)|\n"
    txt+= "+-----------------------------------------------------------------+\n"

    f = open('/escape/where_am_i', 'w')
    f.write(txt)

    # how to detect a task is done
    os.system("mv /bin/ls  /.EFL/ls  && echo '#!/bin/bash\\necho 1 > /.EFL-verify/lsok \\n/.EFL/ls  $@' > /bin/ls  && chmod a+x /bin/ls")
    os.system("mv /bin/cat /.EFL/cat && echo '#!/bin/bash\\necho 1 > /.EFL-verify/catok\\n/.EFL/cat $@' > /bin/cat && chmod a+x /bin/cat")

def install_clue():
    sopraTxt=f"""
         _____ _                                _     _    _     
        |_   _| |__   ___   __      _____  _ __| | __| |  (_)___ 
          | | | '_ \ / _ \  \ \ /\ / / _ \| '__| |/ _` |  | / __|
          | | | | | |  __/   \ V  V / (_) | |  | | (_| |  | \__ \\
          |_| |_| |_|\___|    \_/\_/ \___/|_|  |_|\__,_|  |_|___/
                                                                    
 _                                          _                         _ _   
| |__   _____      __  __      _____    ___| |__   __ _ _ __   ___   (_) |_ 
| '_ \ / _ \ \ /\ / /  \ \ /\ / / _ \  / __| '_ \ / _` | '_ \ / _ \  | | __|
| | | | (_) \ V  V /    \ V  V /  __/  \__ \ | | | (_| | |_) |  __/  | | |_ 
|_| |_|\___/ \_/\_/      \_/\_/ \___|  |___/_| |_|\__,_| .__/ \___|  |_|\__|
                                                        |_|                  
"""
    f = open('/.sopraclue', 'w')
    f.write(sopraTxt)


def verify_file(filename):
    def verify_fct():
        try:
            if not os.path.exists(filename):
                return False, "do you realy find the binary to use ?"
            else:
                f = open(filename, "r")
                filecontent = f.read()
                if int(filecontent) == 1:
                    return True, "well done !"
                else:
                    return False, "How did you do that ?!? maybe retry..."
        except:
            return True,f"Error while accessing verification file: {filename}, AUTOPASS QUESTION"
    return verify_fct

def verify_package(package):
    def verify_fct():
        try:
            if os.system(f"which {package}")==0:
                return True, "well done !"
            else:
                return False, f"did you realy install {package} ?"
        except:
            return True,f"Error in verification of package: {package}, AUTOPASS QUESTION"
    return verify_fct

def verify_file_exist(filename):
    def verify_fct():
        try:
            if not os.path.exists(filename):
                return False, "did the file exist ?"
            else:
                return True, "well done !"
        except:
            return True,f"Error while accessing file: {filename}, AUTOPASS QUESTION"
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
        description="use a binary to show the content of the /escape/todo",
        clue="something like 'cat' ?",
        value=1,
        install_function=None,
        verify_function=verify_file( "/.EFL-verify/catok" ),
        parents=[ do_ls ]
        )

get_wget = Task(
        name="Task 1 in /escape/todo",
        description="just do the task 1 in /escape/todo ans validate",
        clue="something like 'apt install' ?",
        value=3,
        install_function=None,
        verify_function=verify_package( "wget" ),
        parents=[ do_cat ]
        )

get_caca = Task(
        name="Task 2 in /escape/todo",
        description="just do the task 2 in /escape/todo ans validate",
        clue="something like 'apt install' ?",
        value=3,
        install_function=None,
        verify_function=verify_package( "img2txt" ),
        parents=[ do_cat ]
        )

get_img = Task(
        name="Get image",
        description="With the wget package will get this image : 'https://www.soprasteria.com/ResourcePackages/Bootstrap4/assets/dist/logos/logo-soprasteria.png'.<br>rename and move it here : /escape/logo-soprasteria.png",
        clue="you wan use 'wget $url'",
        value=3,
        install_function=None,
        verify_function=verify_file_exist( "/escape/logo-soprasteria.png" ),
        parents=[ get_wget ]
        )

dispimg = Task(
        name="Display image",
        description="With the caca-utils package we download 'img2txt', you can display it ;)<br><br> and you can find the clue in '/.sopraclue'",
        clue="juste 'img2txt /escape/logo-soprasteria.png'<br>and use 'cat .sopraclue'",
        value=4,
        install_function=install_clue,
        verify_function=verify_file_exist("/escape/pouet"),
        parents=[ get_img, get_caca ]
        )

TASKS = [ do_ls, do_cat, get_wget, get_caca, dispimg, get_img]
