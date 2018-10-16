# Setup Webserver:
ssh to the machine where you want to setup webserver and follow the following insructions.

### apache & cgi-bin 
```
#install - cgi-bin 
apt-get update
apt-get install apache2
```

Then paste the following lines in /etc/apache2/sites-enabled/000-default.conf or /etc/apache2/sites-enabled/default.conf
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

### MongoDB
Following steps will install MongoDB and python-api pacakge. In case MongoDB is installed on a separate machine, update do_mongo.py file accordinly [replace localhost with the ipaddress](https://github.com/akhtarnabeel/ecoforecastCS/blob/master/webserver/web/do_mongo.py#L9)
```apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
apt-get update
apt-get install -y mongodb-org
apt-get install python-pip
pip install pymongo
```

Then create a database in mongodb by going to shell and typing 
```$mongo``` 
and then 
```$use NAME_OF_DATABASE```
and then create collections ```users``` and ```results```

### Code and configuration

Go to ```www``` folder usually the path is something like (/var/www/html or /var/www/) and execute 
```
git clone https://github.com/akhtarnabeel/ecoforecastCS.git
```
Then change the database-name/IPs in files do_mongo.py and wrapper.py.

After that restart the apache server. your webpage will be live at ```IP-OF-MACHINE/ecoforecastCS/webserver/web```.
