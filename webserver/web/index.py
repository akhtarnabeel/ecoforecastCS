#!/usr/bin/python
import cgi
import cgitb; cgitb.enable()
import time
import Cookie
import os
import string
import random
from print_pages import *
from do_mongo import *
#from do_whisk import *



def set_cookie(email, work_dir):
	cookie = Cookie.SimpleCookie()
	cookie["remember_me"] = work_dir
	cookie["email"] = email
	print cookie

def do_authenticate(form):
	email = form["email"].value
	#check from database
	work_dir = mongo_do_authenticate(email)
	set_cookie(email, work_dir)

	return True

def create_job(form, cookie):

	user_dir = cookie["remember_me"].value
	r_code = form["r_code"].value
	transaction_dir = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
	os.system("mkdir users/" +user_dir+"/"+transaction_dir)
	git_libs = form["job_git_libs"].value
	cran_libs = form["job_cran_libs"].value
	fileitem = form['file']
	repeat_interval = -1
	end_date = form["end_date"].value

	if fileitem.filename != "":
		#show_error_page(form)
		fn = os.path.basename(fileitem.filename)
		f = open("users/"+user_dir+"/"+ transaction_dir+"/supportingfiles.zip", 'wb')
		f.write(fileitem.file.read())
		f.close()

	if form["repeat_it"].value == "Yes":
		try:
			repeat_interval = int(form["run_interval"].value)*60
		except:
			pass


	print_header()
	print "<br>Transaction Folder: "
	print "<br>users/"+user_dir+"/"+ transaction_dir
	print "<br>Git Libs :" + git_libs 
	print "<br>Cran Libs :" + cran_libs 
	print "<br>Interval: " + str(repeat_interval)
	print "<br>End date: " + str(end_date)





if __name__=="__main__":
	cookie = Cookie.SimpleCookie()
	try:
		cs = os.environ["HTTP_COOKIE"]
		#create cookie object
		cookie.load(cs)
	except:
		pass
	# get form fields
	form = cgi.FieldStorage()
	if "remember_me" in cookie:

		if "new_exp" in form:
			show_lib_page()

		elif "show_old" in form:
			show_test_page()

		elif "code_libs" in form:
			cran_libs = ""
			git_libs = ""
			if "cran_libs" in form:
				cran_libs = form["cran_libs"].value
			if "git_libs" in form:
				git_libs = form["git_libs"].value
			show_submit_code_page(cran_libs, git_libs)

		elif "submit_job" in form:
			if form["r_code"].value != "":
				create_job(form, cookie)
			else:
				show_error_page("Ever consider submitting code?")

		else:
			show_home_page()



	elif "login_button" in form:
		if do_authenticate(form):
			show_home_page()

	else:
		show_login_page()
