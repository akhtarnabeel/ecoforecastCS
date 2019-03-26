#!/usr/bin/python
# import socket programming library

# import thread module
from thread import *
import threading
from shutil import copyfile

# others
import docker
import ast
import logging, cgi
import cgitb; cgitb.enable()
import os, sys
import requests
import configparser; config = configparser.ConfigParser();config.read('../config.ini')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', filename='container_maker.log', filemode='a')






def send_to_server(message):
        logging.info('sending sever:'+str(message))
        r = requests.post(config['web-server']['do_whisk_ip'], data=message)




def build_container(form):

	cran_libraries = ast.literal_eval(form['cran_lib'].value)
	git_libraries  = ast.literal_eval(form['git_lib'].value)
	code_dir = form['code_dir'].value
	code_name = form['code_name'].value
	trigger_name = form['trigger_name'].value

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
			f.write("""RUN R -q -e "install.packages('{0}', dependencies=TRUE, repos='http://cran.rstudio.com/')"\n""".format(depend))

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
		logging.exception('created container sucessfully!')
		# send server a signal
		send_to_server({'code_name': code_name, 'code_dir': code_dir, 'container_ready': 'yes', 'trigger_name':trigger_name})
    	except:
		logging.exception('Error is creating container!')
		return






def authenticate_request(token):
        return True

if __name__== "__main__":

        form = cgi.FieldStorage()
        logging.info('received:' + str(form))

	try:
        	token = form['token']
        	if authenticate_request(token):
			build_container(form)
		else:
			logging.info('Auth failed')
	except:
		print 'No Token!'
