# Setup OpenWhisk
- Assuming Ubuntu installation:

```
# Install git if it is not installed
sudo apt-get install git -y

# Clone openwhisk
git clone https://github.com/akhtarnabeel/incubator-openwhisk.git openwhisk

# Change current directory to openwhisk
cd openwhisk
```

  - Open JDK 8 is installed by running the following script as the default Java environment.

```
# Install all required software
(cd tools/ubuntu-setup && ./all.sh)
```

  - Install dependencies

```
sudo apt-get install python-pip
sudo pip install ansible==2.5.2
sudo pip install jinja2==2.9.6
````

  - Change RAM and time cap:
    
    ```
    ~/openwhisk/incubator-openwhisk/common/scala/src/main/resources/application.conf
    ```

    This file holds the RAM and action time limit. Change the following values to what you want, we've been using a max of 8GB for:
    
    For RAM:
    ```
    # action memory configuration
    memory {
        min = 128 m
        max = 8192 m
        std = 512 m
    }
    ```
    
    For Action Time:
    ```
    # action timelimit configuration
    time-limit {
        min = 100 ms
        max = 1440 m
        std = 5 m
    }
    ```
    
    For Action Time Log:
    ```
    # action log-limit configuration
    log-limit {
        min = 0 m
        max = 1440 m
        std = 20 m
    }
    ```
  
  - Change number of cores and number of core shares for the system
  
  ```
  cd ~/openwhisk/ansible/group_vars/all
  ```
  change ```numcore: 2
  coreshare: 2 ``` to desired values. 
  
  - Build it. (Might have to run the following command twice!)

  ```
  cd <home_openwhisk>
  ./gradlew distDocker
  ```
  - Install the alarm package (Note: this is quite tricky and OpenWhisk does not make this easy to do at all, there are a set of Ansible scripts floating around GitHub to do this, but they have been outdated for about a year, I've modified them to work for the current version but they might need to be further edited later): 
  
  ```
  mkdir -p <home_openwhisk>/ansible/roles/alarmstrigger/tasks
  sudo apt install npm
  mv providers.yml <home_openwhisk>/ansible/providers.yml
  mv alarmstrigger.yml <home_openwhisk>/ansible/alarmstrigger.yml
  mv clean.yml <home_openwhisk>/ansible/roles/alarmstrigger/tasks/clean.yml
  mv deploy.yml <home_openwhisk>/ansible/roles/alarmstrigger/tasks/deploy.yml
  mv main.yml <home_openwhisk>/ansible/roles/alarmstrigger/tasks/main.yml
  mv installProviderActions.yml <home_openwhisk>/ansible/tasks/installProviderActions.yml
  ```
  - Now the group vars for ansible need to be edited for the alarms package:
    
    ```
    TODO
    ```
    
    
  - Using Ansible now:
  
  ```
  Go to ansible folder in openwhisk and 
  sudo ansible-playbook setup.yml
  ```
  
  - Run other Ansible code now:
  
  ```
  cd ansible
  sudo ansible-playbook couchdb.yml
  sudo ansible-playbook initdb.yml
  sudo ansible-playbook wipe.yml
  sudo ansible-playbook openwhisk.yml

  # installs a catalog of public packages and actions
  sudo ansible-playbook postdeploy.yml
  
  # installs alarm package
  sudo ansible-playbook providers.yml

  # to use the API gateway
  sudo ansible-playbook apigateway.yml
  sudo ansible-playbook routemgmt.yml
  ```
  
  - Configure CLI:
    > The API host can be acquired from the edge.host property in whisk.properties file. Use its value below
  
      ```
      ./bin/wsk property set --apihost <openwhisk_baseurl>
      ```
    > Add guest authentication
    
     ```
     ./bin/wsk property set --auth `cat ansible/files/auth.guest`
     ```
     Run 'wsk property get --auth' to see the new value.
  
  - Change local environment to include openwhisk. E.g. add following to the file ~/.profile
  
  ```
  # add path to OpenWhisk
  export PATH=$PATH:/home/nabeel/openwhisk/bin
  # source the file
  source ~/.profile 
  ```
  
- Setup in complete. Now run hello world to see if everything is working file. Make sure to use " -i " in wsk commands for bypassing certificate checking
https://github.com/apache/incubator-openwhisk/blob/master/docs/samples.md
