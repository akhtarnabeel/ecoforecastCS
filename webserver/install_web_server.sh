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


apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
apt-get update
apt-get install -y mongodb-org
pip install pymongo
