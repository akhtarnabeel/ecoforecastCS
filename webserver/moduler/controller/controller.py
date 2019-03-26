#!usr/bin/python

import configparser; config = configparser.ConfigParser();config.read('config.cfg')


if __name__=="__main__":
	print type(config['web-server']['port'])
