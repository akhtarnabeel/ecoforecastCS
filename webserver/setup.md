# Setup Webserver:
ssh to the machine where you want to setup webserver and follow the following insructions.

### apache & cgi-bin 
```
#install - cgi-bin 
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

### MongoDB
Following steps will install MongoDB and python-api pacakge. In case MongoDB is installed on a separate machine, update do_mongo.py file accordinly [replace localhost with the ipaddress](https://github.com/akhtarnabeel/ecoforecastCS/blob/master/webserver/web/do_mongo.py#L9)
```apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
apt-get update
apt-get install -y mongodb-org
apt-get install python-pip
pip install pymongo
```

// add authrntication for mangoDB

Now we need to create database and tables for the database. One can create a database in mongodb by going to shell and typing 
```
mongo
```
In case mongo command doesn't work, look at the [stackoverflow post to fix the issue](https://stackoverflow.com/questions/13312358/mongo-couldnt-connect-to-server-127-0-0-127017)

Create database with name *EcoForecast*. Note that if you chose a different database name, you should update it in [*do_mongo.py*](https://github.com/akhtarnabeel/ecoforecastCS/blob/c260f93557115b49c50b7dec1582def052796d93/webserver/web/do_mongo.py#L10) file.
```
use EcoForecast
```
Right now we are using two main collections (also known as tables);
users: to store user related data
results: to store data for each experiment a user runs in our system (time, name, results etc.). 
Create these tables by running following commands on the mongo shell ([More information on MongoDB and how to create collections](https://www.tutorialspoint.com/mongodb/mongodb_create_collection.htm). Also, it's easy to manipulate MongoDB with some UI based client such as [Compass](https://www.mongodb.com/products/compass))
```
db.createCollection("users")
db.createCollection("results")
```

### Code and configuration

Go to ```www``` folder usually the path is something like (/var/www/html or /var/www/) and execute 
```
git clone https://github.com/akhtarnabeel/ecoforecastCS.git
```
Then change the database-name/IPs in files do_mongo.py and wrapper.py.
Create a folder named as 'users' withen 'web' folder and grant web users permission,
```chown www-data:www-data users```

Also execute the following commands to give cgi-bin permission to all the python files and execute following in 'web' folder
 
 ```
 sudo chmod 755 *.py 
 sudo chmod 755 *.html 
 ```

Also install OpenWhisk client on the webserver machine and set authentication and apihost.
After that restart the apache server. your webpage will be live at ```IP-OF-MACHINE/ecoforecastCS/webserver/web```.
