#!/usr/bin/python

import cgi #"common gateway interface"
import cgitb; cgitb.enable() #CGI traceback
import subprocess #for calling openwhisk
import os 

def print_header():
	print "Content-type: text/html"
	print
	print "<html><head>"
	print "</head><body>"


def print_form():
	 print '''<center><form enctype="multipart/form-data"  method="post">
        <textarea placeholder="Paste your R code here!!!" name="r_code" style="background:#C9F8A3;width:100%;height:75%;wrap:" hard";"=""></textarea>
	<br>Supporting file (.zip): <input type="file" name="file">
                        <input type="submit" name="Submit Code" value="Submit Code">
                        </form></center>'''
def print_r_code(code, fn):
    zip(code, fn)
    out = whisk()
    print "Content-type: text/html"
    print
    f = open("output.json", 'wb')
    f.write(out)
    f.close()
    print '''<a href="output.json" download> Download Output (Json File)</a> <br><br><br><br><br>'''
    print out

def zip(code, fn):
    with open('code.R', 'w') as file:
        file.write(code)
    if fn != "-1":
    	process = subprocess.Popen("cp wrapper.py exec; chmod +x exec; zip temp.zip code.R exec "+fn+"/*", shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    else:
	process = subprocess.Popen("cp wrapper.py exec; chmod +x exec; zip temp.zip code.R exec ", shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
def whisk():
    #Create action
    process = subprocess.Popen(["./wsk", "-i", "action", "create", "temp", "temp.zip", "-m", "8000", "--docker", "alexfarra/ecoforecastdocker:master"], shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    process.wait()
    #Invokes action
    process = subprocess.Popen(["wsk", "-i", "action", "invoke", "temp", "--result", "--blocking"], shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #Returns result of action
    process.wait()
    out = process.stdout.read()
    #remove the temporary action
    process = subprocess.Popen(["./wsk", "-i", "action", "delete", "temp"], shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    process.wait()
    return out

if __name__ =="__main__":
	form = cgi.FieldStorage()
	if "r_code" in form:
		fn = "-1"
		if 'file' in form:
			fileitem = form['file']
			fn = os.path.basename(fileitem.filename)
			f = open("supportingDoc/"+fn, 'wb')
			f.write(fileitem.file.read())
			f.close()
			os.system("unzip supportingDoc/"+fn +" "+fn[-4])
		if fn != "-1":
			print_r_code(form["r_code"].value, fn[-4])
		else:
			print_r_code(form["r_code"].value, fn)

	else:
		print_header()
		print_form()
