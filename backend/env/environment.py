import os
import sys

#path = "/var/www/sites/mysite/backend/env/envtxt.txt"
path = ".\env\envtxt.txt"

class Environment_Variable:
    
    def __init__(self):
        super().__init__()

    def get_val(self, key):
        KEY_VALUE = {}
        print("CWD:", os.getcwd())
        with open(path,'r') as f:
            for line in f:
                if line is None:
                    pass
                splitLine = line.split()
                KEY_VALUE[splitLine[0]] = splitLine[1]            

        return KEY_VALUE[key]
