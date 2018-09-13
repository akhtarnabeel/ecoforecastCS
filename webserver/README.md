# Setup Webserver:

'''
#install - cgi-bin 
apt-get update
apt-get install apache2

# then paste the following lines in /etc/apache2/sites-enabled/000-default.conf or /etc/apache2/sites-enabled/default.conf
#  <Directory /var/www/html/>
#                 Options ExecCGI Indexes FollowSymLinks MultiViews
#                 AllowOverride None
#                 Order allow,deny
#                 allow from all
#                 AddHandler cgi-script .py .html
#  </Directory>

a2enmod cgi
service apache2 restart


apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
apt-get update
apt-get install -y mongodb-org
apt-get install python-pip
pip install pymongo
'''
