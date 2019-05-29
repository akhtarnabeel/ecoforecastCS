# [OUTDATED. Use python ContainerMaker.py file only]
# Container Maker Setup 

1. First install docker using instructions on docker website
https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository

2. Install docker-py using pip
```
pip install docker
```
3. Then setup the Apache server;

```#install - cgi-bin 
apt-get update
apt-get install apache2
```

Then paste the following lines in */etc/apache2/sites-enabled/000-default.conf* or */etc/apache2/sites-enabled/default.conf*
```
<Directory /var/www/html/>
                 Options ExecCGI Indexes FollowSymLinks MultiViews
                 AllowOverride None
                 Order allow,deny
                 allow from all
                 AddHandler cgi-script .py .html
</Directory>
```

Then execute the following commands in the shell.

```
a2enmod cgi
service apache2 restart
```

4. ```cd \var\www\html```
5.  copy the container maker folder from web-server
5. ```cd container-maker```
6. ``` chmod 755 * ```
7. Specify this url 'ip-of-machine'\build_image.py in configuration file on web-sever as well as update the web-server address in the config file in container-maker folder on this machine.



