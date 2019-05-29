#!/usr/bin/python

import os
import zipfile
import subprocess
import docker
import pymongo
import time
import shutil
from pymongo import MongoClient
from dotenv import load_dotenv
import threading
import socket
import logging
import json

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                    filename='EcoForecast.log', filemode='a')

zipname = "supportingfiles.zip"

ContainerIP = '192.1.242.39'
ContainerPort = 12345
ContainerNodePassword = 'sadsafsdad21312423ewdsdfa'

"""
@param user_id: string
@param code: string
@param libraries: list of strings
@param intervals: int in minutes
@param code_dir: string
"""


def run_code(action_name, branch, trigger_name=None, dockerfile='alexfarra/ecoforecastdocker:master'):
    with open("runlogs2.txt", 'w') as f:
        cmd = f'/bin/wsk -i action create {action_name} {zipname} -m 8000 -t 86400000 --docker {dockerfile}'
        p = subprocess.Popen(cmd, stdout=f, stderr=f, shell=True)
        p.wait()
        if (trigger_name != None):
            rule_name = 'rule-' + str(action_name)
            cmd = 'wsk -i rule create ' + \
                str(rule_name) + ' ' + str(trigger_name) + \
                ' ' + str(action_name)
            p = subprocess.Popen(cmd, stdout=f, stderr=f, shell=True)
            p.wait()
        cmd = 'wsk -i action invoke ' + str(action_name)
        p = subprocess.Popen(cmd, stdout=f, stderr=f, shell=True)
        p.wait()


def set_whisk_props():
    openwhisk_ip = os.getenv("OPENWHISK_IP")
    openwhisk_auth = os.getenv("OPENWHISK_AUTH")
    os.system(f"wsk -i property set --apihost {openwhisk_ip}")
    os.system(f"wsk -i property set --auth {openwhisk_auth}")

# Done


def create_wrapper(user_id, transaction_id, model_name, intervals, stop_date):
    set_whisk_props()
    home = os.getenv("HOME_PATH")
    os.system(f'cp {home}/wrapper.py exec')
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_source = os.getenv("DB_NAME")
    db_ip = os.getenv("DB_IP")
    db_port = os.getenv("DB_PORT")
    prefix = f"""
#!/usr/bin/python

db_ip = '{db_ip}'
db_port = {db_port}
db_username = '{db_username}'
db_password = '{db_password}'
db_source = '{db_source}'
user_id = '{user_id}'
transaction_id = '{transaction_id}'
model_name = '{model_name}'
interval = '{intervals}'
stop_date = '{stop_date}'
"""

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
            f.write(
                """RUN R -q -e "library(devtools); install_github('{0}')"\n""".format(depend))
    f.write(
        """CMD ["/bin/bash", "-c", "cd actionProxy && python -u actionproxy.py"]""")
    f.close()
    client = docker.from_env()
    client.images.build(path='/var/www/html/ecoforecastCS/webserver/test/{0}'.format(code_dir),
                        tag='alexfarra/ecoforecastdocker:{0}'.format(code_name))
    image = client.images.get(
        'alexfarra/ecoforecastdocker:{0}'.format(code_name))
    client.login(username='alexfarra', password='')
    client.images.push('alexfarra/ecoforecastdocker', tag=code_name)


# TODO
def configure_libraries_server(cran_libraries, git_libraries, code_dir, code_name):
    # connect to server
    host = ContainerIP

    logging.info('Going to send to container make: cran-lib:' +
                 str(cran_libraries) + " git-lib:"+str(git_libraries))

    # Define the port on which you want to connect
    port = ContainerPort

    # create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))

    passcode_server = ContainerNodePassword

    # password sent to server
    s.send(passcode_server.encode('ascii'))

    # messaga received from server
    s_data = s.recv(1024)
    s_data.strip()

    if s_data == 'InvalidCode':
        return False

    s.send(str(cran_libraries).encode('ascii'))
    s_data = s.recv(1024)
    s_data.strip()
    if s_data != 'GotCran':
        s.close()
        return False

    s.send(str(git_libraries).encode('ascii'))
    s_data = s.recv(1024)
    s_data.strip()
    if s_data != 'GotGit':
        s.close()
        return False

    s.send(code_dir.encode('ascii'))
    s_data = s.recv(1024)
    s_data.strip()
    if s_data != 'GotCodeDir':
        s.close()
        return False

    s.send(code_name.encode('ascii'))
    s_data = s.recv(1024)
    s_data.strip()
    if s_data != 'GotCodeName':
        s.close()
        return False

    # make sure it work
    s.send('START'.encode('ascii'))
    s_data = s.recv(1024)
    s_data.strip()
    if s_data == 'END':
        logging.info('Received END from container maker so good to go!')
        s.close()
        return True
    else:
        s.close()
        return False


''' 
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
    client.login(username='alexfarra', password='')
    client.images.push('alexfarra/ecoforecastdocker', tag=code_name)
'''

# Works


def prepend(file1, string):
    with open(file1, 'r') as f:
        with open('temp.txt', 'w') as f2:
            f2.write(string)
            f2.write(f.read())
    os.rename('temp.txt', file1)
    os.system('chmod +x ' + str(file1))


def openwhisk_exec(model_name, user_id, transaction_id, code, code_dir, cran_libraries=None, git_libraries=None,
                   intervals=-1, stop_date=None, dockerfile='alexfarra/ecoforecast:master'):
    # create new thread and run the code
    t = threading.Thread(target=init_openwhisk, args=(
        model_name, user_id, transaction_id, code, code_dir, cran_libraries, git_libraries, intervals, stop_date, dockerfile))
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
    shutil.rmtree(
        '/var/www/html/ecoforecastCS/webserver/test/{0}'.format(code_dir))


def deleteAll(code_dir, transaction_id):
    deleteAction(code_dir)
    deleteDatabase(transaction_id)
    deleteDir(code_dir)


def init_openwhisk(model_name, user_id, transaction_id, code, code_dir, cran_libraries=None, git_libraries=None,
                   intervals=-1, stop_date=None, dockerfile='alexfarra/ecoforecast:master'):
    '''
    initialize and run openWhisk
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
        # default container branch is master
        branch = 'master'
        # creating code name
        code_name = code_dir.replace("/", "")
        # creating action name
        action_name = str(code_name)
        trigger_name = None
        # create wrapper for the code and save it as exec
        create_wrapper(user_id, transaction_id,
                       model_name, intervals, stop_date)

        create_code(code)

        # Set intervals for running triggers
        if intervals > 0:
            stop_date = str(stop_date) + "T23:59:00.000Z"
            trigger_name = configure_intervals(
                action_name, intervals, stop_date)
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
            if (configure_libraries_server(cran_libraries, git_libraries, code_dir, code_name) == False):
                logging.info("Error: Cannot create container with libraries")
                return
            logging.info('Container created')
            # name used for locating docker container
            branch = code_name

        # run the openWhisk code
        logging.info('Creating Action and Triggering it')
        run_code(action_name, branch, trigger_name, dockerfile)
        logging.info('Action code is Triggered...')
    except:
        logging.exception("ERROR in running OpenWhisk job...")


test = {"Image": "Nabeel no error!"}
print(json.dumps(test))

#configure_libraries_server([], ["khufkens/MODISTools"], "Test2", "WithLibraries")

#logging.exception("ERROR in running OpenWhisk job...")
