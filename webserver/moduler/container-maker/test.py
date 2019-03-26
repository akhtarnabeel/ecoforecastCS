import requests
r = requests.post(" http://192.1.242.151/ecoforecastCS/webserver/moduler/container-maker/build_image.py", data={'cran_lib': str([]), 'git_lib': str([]), 'token': 'yes' , 'user_name': 'show', 'exp_name': 'yes'})
