#!/usr/bin/python

import os
import zipfile
import subprocess
import docker
import pymongo
import time
import shutil
from pymongo import MongoClient
import threading
import socket
import logging
import requests
import cgi
import cgitb; cgitb.enable()
import configparser; config = configparser.ConfigParser();config.read('config.ini')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', filename='EcoForecast.log',
                    filemode='a')

zipname = "supportingfiles.zip"

MongoIP = '192.1.242.151'
MongoPort = 27017

ContainerIP = '192.1.242.34'
ContainerPort = 12345
ContainerNodePassword = 'sadsafsdad21312423ewdsdfa'

"""
@param user_id: string
@param code: string
@param libraries: list of strings
@param intervals: int in minutes
@param code_dir: string
"""

def send_message(server, message):
        logging.info('sending container maker:'+ str(message))
        r = requests.post(server, data=message)
	return True


def run_code(action_name, branch, trigger_name=None, open_whisk_ip = None):
    #update stuff according to open_whisk_ip
    with open("runlogs2.txt", 'w') as f:
        cmd = '/bin/wsk -i action create ' + str(action_name) + ' ' + str(
            zipname) + ' -m 8000 --docker alexfarra/ecoforecastdocker:{0}'.format(branch)
        p = subprocess.Popen(cmd, stdout=f, stderr=f, shell=True)
        p.wait()
        if (trigger_name != None):
            rule_name = 'rule-' + str(action_name)
            cmd = 'wsk -i rule create ' + str(rule_name) + ' ' + str(trigger_name) + ' ' + str(action_name)
            p = subprocess.Popen(cmd, stdout=f, stderr=f, shell=True)
            p.wait()
        cmd = 'wsk -i action invoke ' + str(action_name)
        p = subprocess.Popen(cmd, stdout=f, stderr=f, shell=True)
        p.wait()


# Done
def create_wrapper(user_id, transaction_id, model_name, intervals, stop_date):
    # os.system("wsk -i property set --apihost 129.114.109.157")
    # os.system("wsk -i property get --auth 23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP")
    os.system('cp /var/www/html/ecoforecastCS/webserver/test/wrapper.py exec')
    prefix = """#!/usr/bin/python
user_id = '""" + str(user_id) + """'
transaction_id = '""" + str(transaction_id) + """'
model_name = '""" + str(model_name) + """'
interval = '""" + str(intervals) + """'
stop_date = '""" + str(stop_date) + """'"""
    prepend('exec', prefix)


# Done
def create_code(code):
    f = open("code.R", "w")
    f.write(code)
    f = open("code.R", "rw")
    with zipfile.ZipFile(zipname, 'a') as z:
        z.write('code.R')
        z.write('exec')


# TODO
def configure_intervals(action_name, intervals, stop_date):
    with open("runlogs.txt", 'w') as f:
        cmd = "wsk -i trigger create interval-" + str(
            action_name) + " --feed /whisk.system/alarms/interval --param minutes " + str(
            intervals) + " --param stopDate " + '"' + str(stop_date) + '"'
        trigger_name = "interval-" + str(action_name)
        p = subprocess.Popen(cmd, stdout=f, stderr=f, shell=True)
        p.wait()
    return trigger_name


# TODO
def configure_libraries(cran_libraries, git_libraries, code_dir, code_name):
    f = open("Dockerfile", "w")
    f.write("FROM alexfarra/ecoforecastdocker:master\n")
    for depend in cran_libraries:
        if depend != '':
            f.write(
                """RUN R -q -e "install.packages('{0}', dependencies=TRUE, repos='http://cran.rstudio.com/')"\n""".format(
                    depend))
    for depend in git_libraries:
        if depend != '':
            f.write("""RUN R -q -e "library(devtools); install_github('{0}')"\n""".format(depend))
    f.write("""CMD ["/bin/bash", "-c", "cd actionProxy && python -u actionproxy.py"]""")
    f.close()
    client = docker.from_env()
    client.images.build(path='/var/www/html/ecoforecastCS/webserver/test/{0}'.format(code_dir),
                        tag='alexfarra/ecoforecastdocker:{0}'.format(code_name))
    image = client.images.get('alexfarra/ecoforecastdocker:{0}'.format(code_name))
    client.login(username='alexfarra', password='draco115')
    client.images.push('alexfarra/ecoforecastdocker', tag=code_name)


# TODO
def configure_libraries_server(cran_libraries, git_libraries, code_dir, code_name, trigger_name):
	container_make_ip = config['container_make']['ip']
	token = config['others']['container-token']
	mess = {}
	mess['token'] = token
	mess['code_dir'] = str(code_dir)
	mess['code_name'] = str(code_name)
	mess['cran_lib'] = str(cran_libraries)
	mess['git_lib'] = str(git_libraries)
	mess['trigger_name'] = str(trigger_name)
	return send_message(container_make_ip, mess)

# Works
def prepend(file1, string):
    with open(file1, 'r') as f:
        with open('temp.txt', 'w') as f2:
            f2.write(string)
            f2.write(f.read())
    os.rename('temp.txt', file1)
    os.system('chmod +x ' + str(file1))


def openwhisk_exec(model_name, user_id, transaction_id, code, code_dir, cran_libraries=None, git_libraries=None,
                   intervals=-1, stop_date=None):
    # create new thread and run the code
    t = threading.Thread(target=init_openwhisk, args=(
    model_name, user_id, transaction_id, code, code_dir, cran_libraries, git_libraries, intervals, stop_date))
    t.start()


def deleteAction(code_dir):
    action_name = code_dir.replace("/", "")
    os.system("wsk -i action delete {0}".format(action_name))
    os.system("wsk -i trigger delete interval-{0}".format(action_name))
    os.system("wsk -i rule delete rule-{0}".format(action_name))


def deleteDatabase(transaction_id):
    client = MongoClient(MongoIP, MongoPort)
    db = client.EcoForecast
    results = db.results
    results.remove({'transaction_id': transaction_id})


def deleteDir(code_dir):
    shutil.rmtree('/var/www/html/ecoforecastCS/webserver/test/{0}'.format(code_dir))


def deleteAll(code_dir, transaction_id):
    deleteAction(code_dir)
    deleteDatabase(transaction_id)
    deleteDir(code_dir)


def init_openwhisk(model_name, user_id, transaction_id, code, code_dir, cran_libraries=None, git_libraries=None,
                   intervals=-1, stop_date=None):
    '''
    initialize and run openWhish
    :param model_name: name of model
    :param user_id: user id defined
    :param transaction_id:
    :param code: name of file with code
    :param code_dir: directory where code is
    :param cran_libraries: cran libraries needed
    :param git_libraries: git libraries needed
    :param intervals:
    :param stop_date:
    :return:
    '''

    logging.info('Initializing OpenWhisk...')

    try:
        # create code directory
        if not os.path.isdir(code_dir):
            os.mkdir(code_dir)
        # change to current working directory to code directory
        os.chdir(code_dir)
	# brach is master always by default
	branch = "master"
        # creating code name
        code_name = code_dir.replace("/", "")
        # creating action name
        action_name = str(code_name)
        trigger_name = None
        # create wrapper for the code and save it as exec
        create_wrapper(user_id, transaction_id, model_name, intervals, stop_date)

        create_code(code)

        # Set intervals for running triggers
        if intervals > 0:
            stop_date = str(stop_date) + "T23:59:00.000Z"
            trigger_name = configure_intervals(action_name, intervals, stop_date)
        # Install cran and git libraries
        if cran_libraries != "" or git_libraries != "":
            logging.info("Creating container with required libraries")
            cran_libraries = cran_libraries.replace(" ", "")
            cran_libraries = cran_libraries.split("\n")
            git_libraries = git_libraries.replace(" ", "")
            git_libraries = git_libraries.split("\n")
            # install libraries
            # configure_libraries(cran_libraries, git_libraries, code_dir, code_name)
            logging.info('Calling container function')
            if (configure_libraries_server(cran_libraries, git_libraries, code_dir, code_name, trigger_name) == False):
                logging.info("Error: Cannot create container with libraries")
                return
            logging.info('Container being created ...')
	    return # in case we are waitng for container, dont execute the code right away, waiting for reply and then calling run_code from main

        # run the openWhisk code
        logging.info('Running Code ...')
        run_code(action_name, branch, trigger_name)

    except:
        logging.exception("ERROR in running OpenWhisk job...")


def run_on_reply(form):
	code_name = form['code_name'].value 
	code_dir = form['code_dir'].value
	trigger_name= form['trigger_name'].value
	action_name = code_name
	branch = code_name
	try:
		 # run the openWhisk code
        	logging.info('Running Code')
		# call to cotroller giving us ip of openwhisk
        	run_code(action_name, branch, trigger_name)

    	except:
        	logging.exception("ERROR in running OpenWhisk job...")

	# check form config if debug
	# remove all the data folder code _dir

if __name__ == "__main__":
	form = cgi.FieldStorage()
	if 'container_ready' and 'code_name' and 'code_dir' and 'trigger_name' in form:
		logging.info('Recived from container make', form)
		run_on_reply(form)
	else:
		logging.info('Error from container maker:', form)

#configure_libraries_server([], ["khufkens/MODISTools"], "Test2", "WithLibraries")

