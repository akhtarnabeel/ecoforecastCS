#!/usr/bin/python


def print_header():
	print "Content-type: text/html"
	print 
	print '''<head>
  		<link rel="stylesheet" type="text/css" href="style.css">
	</head>'''



def show_add_library_page():
	print_header()
	print "I am library Page"


def show_test_page():
	print_header()
	print "I am test page"


def show_login_page():
	print_header()
	print """ 
    <h2>Welcome</h2>
    You must identify yourself to use this website. Please enter your:
    <p>
    <form method="post">
    <table>
      <tr>
        <td>
          <h3>Email Address:</h3>
        </td>
        <td>
          <input type="text" name="email" size="20"><br>
        </td>
      </tr>
        <td>
        <input type="submit" name="login_button" value="Authenticate">
        </td>
        <td>
        </td>
      </tr>
    </table>
    </form>
    """




def show_home_page():
	print_header()
	print ''' <div id="container">
		<form method="post">
			<input type="submit" id="button1" name="show_old" value="Show Old Results">
			<input type="submit" id="button2" name= "new_exp" value=" Run New Experiment">
		</form>
              </div>'''



def show_lib_page():
	print_header()
	print ''' 

	<form  method="post">
	<center>
	<table>
	<col width="300px">
	<col width="300px">
	<tr>
	<h1>Please specify libraries here!</h1>
	</tr>

	<tr>
	<td>
	Put GitHub Libraries "handle/package-name":
	</td>
	<td>
	Put Cran Libraries "package-name"
	</td>
	<tr>
	<td>
	<textarea placeholder="Github Libraries" name="git_libs" style="background:#C9F8A3;width:300px;height:400px;"></textarea>
	</td>
	<td>
	<textarea placeholder="Cran Libraries" name="cran_libs" style="background:#C9F8A3;width:300px;height:400px;"></textarea>
	</td>
	</tr>
	<tr>
	</tr>
	</table>
             <input type="submit" name="code_libs" value="Submit Libraries">
 	</center>
 
      </form>'''




def show_submit_code_page(cran_libs, git_libs):
	print_header()
	print """ 
         <center><form enctype="multipart/form-data"  method="post">

      	 <input type="hidden" name="job_cran_libs" value="{0}">
	 <input type="hidden" name="job_git_libs" value="{1}">

	<table>
	<col width="900px">
	<col width= "300px">
	<tr>
	<td>
	<h1> Sumbit Your Code here!</h1>
	</td>
	</tr>
	<tr>
	<td>
	Your Model Name: <input type="text" name="model_name" value="name">
	</td>
	</tr>
	<tr>
	<td>
	<textarea placeholder="Paste your R code here!!!" name="r_code" style="background:#C9F8A3;width:900px;height:500px;wrap:" hard";"=""></textarea>
        </td>
	<td>
	Do yo want to repeat this Experiment?<br> <input type="radio" name="repeat_it" value="No" selected> No <input type="radio" name="repeat_it" value="Yes"> Yes<br><br>
	Run it every(hours): <input type="text" name="run_interval" value="00"> <br><br>
	Till: <input type="date" name="end_date"><br><br>
	Supporting file (.zip): <input type="file" name="file" > <br><br><br>
	</td>
	</tr>
	</table>
        <input type="submit" name="submit_job" value="Submit Code">

	</form></center> """.format(cran_libs, git_libs)




def show_error_page(message):
	print_header()
	print message

