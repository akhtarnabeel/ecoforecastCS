#!/usr/bin/python


def print_header():
	print "Content-type: text/html"
	print 

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
	print '''
		<form method="post">
			<input type="submit" name="show_old" value="Show Old Results">
			<input type="submit" name= "new_exp" value=" Run New Experiment">
		</form>
              '''



def show_lib_page():
	print_header()
	print '''

	<form  method="post">
	<table>
	<tr>
	<td>
        Put GitHub Libraries "handle/package-name":
	</td>
	<td>
	Put Cran Libraries "package-name"
	</td>
	<tr>
	<td>
	<textarea placeholder="Github Libraries" name="git_libs" style="background:#C9F8A3;width:40%;height:75%;wrap:" hard";"=""></textarea>
	</td>
	<td>
	<textarea placeholder="Cran Libraries" name="cran_libs" style="background:#C9F8A3;width:30%;height:75%;wrap:" hard";"=""></textarea>
	</td>
	</tr>
	<tr> <center>
             <input type="submit" name="code_libs" value="Submit Libraries">
 	</center>
	</tr>

	</table>
       </form>'''




def show_submit_code_page(cran_libs, git_libs):
	print_header()
	print """

         <center><form enctype="multipart/form-data"  method="post">

      	 <input type="hidden" name="job_cran_libs" value="{0}">
	 <input type="hidden" name="job_git_libs" value="{1}">
	 Code: <textarea placeholder="Paste your R code here!!!" name="r_code" style="background:#C9F8A3;width:100%;height:75%;wrap:" hard";"=""></textarea>
         Do yo want to repeat this: <input type="radio" name="repeat_it" value="No" selected> No <input type="radio" name="repeat_it" value="Yes"> Yes<br>

	 Run it again(hours): <input type="text" name="run_interval" value="00">
	 Till: <input type="date" name="end_date">
	 <br>Supporting file (.zip): <input type="file" name="file" >
         <br>
         <input type="submit" name="submit_job" value="Submit Code">
         </form></center> """.format(cran_libs, git_libs)




def show_error_page(message):
	print_header()
	print message
