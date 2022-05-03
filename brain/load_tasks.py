import importlib
import fnmatch
import inspect
import sys
import os

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result




def load():
    tasks = find('*.py', 'exos')
    packages = [ importlib.import_module('exos') ]
    modules = []
    TASKS = []

    for f in tasks:
        try:
            subpackage_tree = ""
            for subpackage in f.split("/")[:-1]:
                try:
                    print("loading subpackage", f'{subpackage_tree}{subpackage}')
                    packages.append( importlib.import_module( f'{subpackage_tree}{subpackage}' , package='exos' ) )
                    subpackage_tree += f"{subpackage}."
                except Exception as e:
                    print(e)
                    break

            print("loading module", f'{subpackage_tree}{f.split("/")[-1].split(".")[0]}')
            modules.append( importlib.import_module( f'{subpackage_tree}{f.split("/")[-1].split(".")[0]}', package='exos' ) )
        except Exception as e:
            print(e)

    for module in modules:
        TASKS += getattr(module, 'TASKS')

    return TASKS



