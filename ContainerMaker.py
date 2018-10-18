
# import socket programming library
import socket
import os, sys

# import thread module
from thread import *
import threading
import logging

from shutil import copyfile

# others
import docker
import ast



def createContainer(cran_libraries, git_libraries, code_dir, code_name):
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
    client.images.build(path='/var/www/html/ecoforecastCS/webserver/test/{0}'.format(code_dir), tag='alexfarra/ecoforecastdocker:{0}'.format(code_name))
    image = client.images.get('alexfarra/ecoforecastdocker:{0}'.format(code_name))
    client.login(username='alexfarra',password='draco115')
    client.images.push('alexfarra/ecoforecastdocker', tag=code_name)



print_lock = threading.Lock()

passcode_server = 'sadsafsdad21312423ewdsdfa'

# thread fuction
def threaded(c):

    # data received from client
    passcode = c.recv(2048)

    logging.info("serverdata: "+ passcode)

    if passcode.strip() != passcode_server:
        c.send('InvalidCode')
        logging.info("InvalidCode")
        c.close()
        return
    else:
        c.send('SendData')

    cran_lib = c.recv(2048)
    logging.info("serverdata: " + cran_lib)
    cran_libraries = ast.literal_eval(cran_lib)
    c.send('GotCran')

    git_lib = c.recv(2048)
    logging.info("serverdata: " + git_lib)
    git_libraries = ast.literal_eval(git_lib)
    c.send('GotGit')

    code_dir = c.recv(2048)
    logging.info("serverdata: " + code_dir)
    code_dir.strip()
    c.send('GotCodeDir')

    code_name = c.recv(2048)
    logging.info("serverdata: " + code_name)
    code_name.strip()
    c.send('GotCodeName')

    start = c.recv(2048)
    logging.info("serverdata: " + start)
    start.strip()
    if start != "START":
        logging.info('creating container...')

    # create directory
    if not os.path.isdir('/tmp/{0}'.format(code_name)):
        os.mkdir('/tmp/{0}'.format(code_name))

    # go to this directory
    os.chdir('/tmp/{0}'.format(code_name))

    # create container and push it
    f = open("Dockerfile", "w")
    f.write("FROM alexfarra/ecoforecastdocker:master\n")

    # add cran dependencies
    for depend in cran_libraries:
        if depend != '':
            f.write(
                """RUN R -q -e "install.packages('{0}', dependencies=TRUE, repos='http://cran.rstudio.com/')"\n""".format(depend))

    # add git dependencies
    for depend in git_libraries:
        if depend != '':
            f.write("""RUN R -q -e "library(devtools); install_github('{0}')"\n""".format(depend))

    f.write("""CMD ["/bin/bash", "-c", "cd actionProxy && python -u actionproxy.py"]""")
    f.close()

    logging.info("code_dir: {0}".format(code_dir))

    try:
        # create docker
        client = docker.from_env()
        client.images.build(path='/tmp/{0}'.format(code_name), tag='alexfarra/ecoforecastdocker:{0}'.format(code_name))
        client.images.get('alexfarra/ecoforecastdocker:{0}'.format(code_name))
        client.login(username='alexfarra', password='draco115')
        client.images.push('alexfarra/ecoforecastdocker', tag=code_name)
    except:
        logging.exception('Error is creating container!')
        c.send('UNABLE')
        c.close()
        return

    c.send('END')
    c.close()
    logging.info('Container created!')


def Main():

    # start logging
    logging.basicConfig(level = logging.INFO,format = '%(asctime)s %(levelname)s %(message)s',filename = 'ContainerMaker.log',filemode = 'w')

    host = ""

    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((host, port))

    logging.info( "Container maker running at port {0}".format(port) )

    # put the socket into listening mode
    s.listen(5)

    logging.info("Socket is listening...")

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        c, addr = s.accept()

        # # lock acquired by client
        # print_lock.acquire()

        logging.info('Connected to :{0} {1}'.format(addr[0], addr[1]))

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))

    s.close()


if __name__ == '__main__':
    Main()