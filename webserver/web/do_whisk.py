#!/usr/bin/python

import os
import zipfile
import subprocess
import docker
import pymongo
import time
import shutil
from pymongo import MongoClient

zipname = "supportingfiles.zip"

"""
@param user_id: string
@param code: string
@param libraries: list of strings
@param intervals: int in minutes
@param code_dir: string
"""



def run_code(action_name, branch, trigger_name=None):
    with open("runlogs2.txt", 'w') as f:
        cmd = '/bin/wsk -i action create ' + str(action_name) + ' ' + str(zipname) + ' -m 8000 --docker alexfarra/ecoforecastdocker:{0}'.format(branch)
        p = subprocess.Popen(cmd, stdout=f, stderr=f, shell=True)
        p.wait()
        if trigger_name!=None:
            rule_name = 'rule-' + str(action_name)
            cmd = 'wsk -i rule create ' + str(rule_name) + ' ' + str(trigger_name) + ' ' + str(action_name)
            p = subprocess.Popen(cmd, stdout=f, stderr=f, shell=True)
            p.wait()
        cmd = 'wsk -i action invoke ' + str(action_name)
        p = subprocess.Popen(cmd, stdout=f, stderr=f, shell=True)
        p.wait()
    
#Done
def create_wrapper(user_id, transaction_id, model_name, intervals, stop_date):
    #os.system("wsk -i property set --apihost 129.114.109.157")
    #os.system("wsk -i property get --auth 23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP")
    os.system('cp /var/www/html/ecoforecastCS/webserver/web/wrapper.py exec')
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
    with zipfile.ZipFile(zipname, 'a') as z:
        z.write('code.R')
        z.write('exec')
    


#TODO
def configure_intervals(action_name, intervals, stop_date):
    with open("runlogs.txt", 'w') as f:
        cmd = "wsk -i trigger create interval-" + str(action_name) + " --feed /whisk.system/alarms/interval --param minutes " + str(intervals) + " --param stopDate " + '"' + str(stop_date) +  '"'
        trigger_name = "interval-" + str(action_name)
        p = subprocess.Popen(cmd, stdout=f, stderr=f, shell=True)
        p.wait()
    return trigger_name 


#TODO
def configure_libraries(cran_libraries, git_libraries, code_dir, code_name):
    f = open("Dockerfile", "w")
    f.write("FROM alexfarra/ecoforecastdocker:master\n")
    for depend in cran_libraries:
        if depend != '':
            f.write("""RUN R -q -e "install.packages('{0}', dependencies=TRUE, repos='http://cran.rstudio.com/')"\n""".format(depend))
    for depend in git_libraries:
        if depend != '':
            f.write("""RUN R -q -e "library(devtools); install_github('{0}')"\n""".format(depend))
    f.write("""CMD ["/bin/bash", "-c", "cd actionProxy && python -u actionproxy.py"]""")
    f.close()
    client = docker.from_env()
    client.images.build(path='/var/www/html/ecoforecastCS/webserver/web/{0}'.format(code_dir), tag='alexfarra/ecoforecastdocker:{0}'.format(code_name))
    image = client.images.get('alexfarra/ecoforecastdocker:{0}'.format(code_name))
    client.login(username='alexfarra',password='draco115')
    client.images.push('alexfarra/ecoforecastdocker', tag=code_name)
    
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
    branch = 'master'
    code_name = code_dir.replace("/", "")
    action_name= str(code_name)
    trigger_name=None
    create_wrapper(user_id, transaction_id, model_name, intervals, stop_date)
    create_code(code)
    if intervals > 0:
        stop_date = str(stop_date) + "T23:59:00.000Z"
        trigger_name = configure_intervals(action_name, intervals, stop_date)   
    if cran_libraries!="" or git_libraries!="":
        cran_libraries = cran_libraries.replace(" ", "")
        cran_libraries = cran_libraries.split("\n")
        git_libraries = git_libraries.replace(" ", "")
        git_libraries = git_libraries.split("\n")
        configure_libraries(cran_libraries, git_libraries, code_dir, code_name)
        branch = code_name
    run_code(action_name, branch, trigger_name)

def deleteAction(code_dir):
    action_name = code_dir.replace("/", "")
    os.system("wsk -i action delete {0}".format(action_name))
    os.system("wsk -i trigger delete interval-{0}".format(action_name))
    os.system("wsk -i rule delete rule-{0}".format(action_name))

def deleteDatabase(transaction_id):
    client = MongoClient('192.1.242.151', 27017)
    db = client.EcoForecast
    results = db.results
    results.remove({'transaction_id': transaction_id})

def deleteDir(code_dir):
    shutil.rmtree('/var/www/html/ecoforecastCS/webserver/web/{0}'.format(code_dir))

def deleteAll(code_dir, transaction_id):
    deleteAction(code_dir)
    deleteDatabase(transaction_id)
    deleteDir(code_dir)




#R_code = """retJSON <- '{
#  \"msg\": 3
#}'
#write(retJSON, file="out.json")
#cat('TEST')"""
#openwhisk_exec("test", "alex", "4", R_code, "users/alex/4", cran_libraries='slipify\n', git_libraries='EcoForecast/ecoforecastR\n', intervals=2, stop_date='2018-08-14')

#time.sleep(5)

#deleteAll('users/alex/4', '4')




