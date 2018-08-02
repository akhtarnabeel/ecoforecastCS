#!/usr/bin/python

import os
import zipfile
import subprocess

zipname = "supportingfiles.zip"

"""
@param user_id: string
@param code: string
@param libraries: list of strings
@param intervals: int in minutes
@param code_dir: string
"""



def run_code(action_name, trigger_name=None):
    cmd = '/bin/wsk -i action create ' + str(action_name) + ' ' + str(zipname) + ' -m 8000 --docker alexfarra/ecoforecastdocker:master'
    os.system(cmd)
    if not trigger_name==None:
        rule_name = 'rule-' + str(action_name)
        cmd = 'wsk -i rule create ' + str(rule_name) + ' ' + str(trigger_name) + ' ' + str(action_name)
        os.system(cmd)
    cmd = 'wsk -i action invoke ' + str(action_name)
    os.system(cmd)
    
    

#Done
def create_wrapper(user_id, transaction_id, model_name, intervals, stop_date):
    os.system('cp /var/www/html/web/wrapper.py exec')
    prefix = """#!/usr/bin/python
user_id = '""" + str(user_id) + """'
transaction_id = '""" + str(transaction_id) + """'
model_name = '""" + str(model_name) + """'
interval = '""" + str(intervals) + """'
stop_date = '""" + str(stop_date)+ """'""" 
    prepend('exec', prefix)
    

#Done
def create_code(code):
    f = open("code.R","w")
    f.write(code)
    f = open("code.R", "rw")
    with zipfile.ZipFile(zipname, 'w') as z:
        z.write('code.R')
        z.write('exec')
    


#TODO
def configure_intervals(action_name, intervals, end_date):
    cmd = "wsk -i trigger create interval-" + str(action_name) + " --feed /whisk.system/alarms/interval --param minutes " + str(intervals) + " --param stopDate " + '"' + str(end_date) +  '"'
    trigger_name = "interval-" + str(action_name)
    os.system(cmd)
    return trigger_name 


#TODO
def configure_libraries(libraries):
    pass

#Works
def prepend(file1, string):
    with open(file1, 'r') as f:
        with open('temp.txt', 'w') as f2:
            f2.write(string)
            f2.write(f.read())
    os.rename('temp.txt', file1)
    os.system('chmod +x ' + str(file1))


def openwhisk_exec(model_name, user_id, transaction_id, code, code_dir, cran_libraries=None, git_libraries=None, intervals=-1, stop_date=None):
    if not os.path.isdir(code_dir):
        os.mkdir(code_dir)
    os.chdir(code_dir)
    code_name = code_dir.replace("/", "")
    action_name= str(user_id) + str(code_name)
    trigger_name=None
    create_wrapper(user_id, transaction_id, model_name, intervals, stop_date)
    #print("create wrapper")
    create_code(code)
    #if not intervals == -1:
        #trigger_name = configure_intervals(action_name, intervals, end_date)
    #if not cran_libraries==None:
        #configure_libraries(libraries)
    run_code(action_name, trigger_name)




#R_code = """retJSON <- '{
#  \"msg\": 3
#}'
#write(retJSON, file="out.json")"""
#openwhisk_exec("test", "alex", "12345", R_code, "alex/1234")





