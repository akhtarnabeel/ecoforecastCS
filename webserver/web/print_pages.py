#!/usr/bin/python
import json

def print_header():
	print "Content-type: text/html"
	print 
	print '''<head>
  		<link rel="stylesheet" type="text/css" href="style.css">
	</head> <body>'''

def add_main_menue():
	print """  <div class="topnav">
                <a class="active" href="?show_home=true">Home</a>
                <a href="?new_exp=clicked">Start New Exp</a>
                <a href="?show_old=clicked">Show Logs</a>
                <a href="#">Instructions!</a>
                </div>
	"""

def show_add_library_page():
	print_header()
	print "I am library Page"


def show_test_page():
	print_header()
	print "I am test page"


def show_login_page():
	print_header()
	print """<center>
    <h2>Welcome</h2>
    You must identify yourself to use this website. Please enter your:

    <form method="post">
    <table>
      <tr>
        <td>
          Email Address:
        </td>
        <td>
          <input type="text" name="email" size="20"><br>
        </td>
      </tr>

      <tr>
        <td>
          Password:
        </td>
        <td>
          <input type="password" name="pass" size="20"><br>
        </td>
      </tr>

    </table>
        <input type="submit" id="button3" name="login_button" value="login">

    </form> </center>
    """




def show_home_page():
	print_header()
	add_main_menue()
	print ''' 
		<div id="container">
		<form method="post">
			<input type="submit" id="button1" name="show_old" value="Show Old Results">
			<input type="submit" id="button2" name= "new_exp" value=" Run New Experiment">
		</form>
              	</div>'''



def show_lib_page():
	print_header()
	add_main_menue()
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
	add_main_menue()
	print """ 
         <center><form enctype="multipart/form-data"  method="post">

      	 <input type="hidden" name="job_cran_libs" value="{0}">
	 <input type="hidden" name="job_git_libs" value="{1}">

	<table>
	<col width="900px">
	<col width= "300px">
	<tr>
	<td>
	<h1> Submit Your Code here!</h1>
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


def show_all_record_page(records, mes):
	print_header()
	add_main_menue()
	print "<h1> All Records </h1>"

	if mes == "redirect":
		print "<p>if you just submitted a job, refresh this page in a while and you will see the results here!</p>"

	print """<center>
        	<table>
        	<tr> <td>User ID</td> <td>Experiment ID</td> <td>Experiment Name</td> <td>Time</td> <td>Preiodic</td> <td>Results</td></tr>
        	"""

	for rec in records:
		print """<tr>
			<td>{0}</td>
			<td>{1}</td>
			<td>{2}</td>
			<td>{3}</td>""".format(rec['user_id'], rec['transaction_id'], rec['model_name'], rec['time'])

		if rec["interval"] != "-1":
			print "<td>Yes</td>"
		else:
                	print "<td>No</td>"

                print """<td><a href="?user_id={0}&&transaction_id={1}&&show_one_result=True">View Results</a></td>
                	</tr>""".format(rec['user_id'], rec['transaction_id'])

	print """ </center>
		</table>"""






def show_error_page(message):
	print_header()
	print message


def get_all_variables(file_path):
        with open(file_path) as f:
                data = json.load(f)
                return data["body"].keys()


def show_one_result(user_id):
	print_header()
	add_main_menue()
	print "The result (Download Json file)"
	print '''<a href="users/%s/view_results/view.json" download> Download </a> <br>'''.format(user_id)

	try:
		all_variables = get_all_variables("users/"+user_id+"/view_results/view.json")
	except:
		print "There was no body in json"
		return

	print """ 

	<html>  
		<head>
    		<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
    	<script type="text/javascript">
        function plot_this(){
        var e = document.getElementById("x_var");
        var x_to_plot = e.options[e.selectedIndex].text;
        var e = document.getElementById("y_var");
        var y_to_plot = e.options[e.selectedIndex].text;
        var xdata = null;var ydata = null;
        var xlab = null;
        var ylab = null;        //var graphtitle = null"""
        #$.getJSON('"""
	print "$.getJSON(\'users/"+user_id+"/view_results/view.json\'"
	print """ , function(data) {
	xdata = data.body[x_to_plot];
        console.log(data.body.x);
        ydata = data.body[y_to_plot];
        xlab = data.xlab;
        ylab = data.ylab;
        //graphtitle = data.graphtitle;
        var trace1 = {
                x: xdata,
                y: ydata, 
                mode: 'markers'
        };
        var data = [ trace1 ];

        var layout = {
        xaxis: {
        title: xlab
        },
        yaxis: {
        title: ylab
        },
        //title: graphtitle
        };
        Plotly.newPlot('myDiv', data, layout);
        });


      }

	</script>
  	</head>	
	<body>
    <table>
   <tr>
   <center> Plot these results! <br>
    <form name="myform" action="javascript:plot_this()">
    <select id="x_var">"""


	for i in all_variables:
        	print """ 
         <option value="{0}">{0}</option> 
        """.format(i)
	print """</select> VS <select id="y_var">"""

	for i in all_variables:
        	print """ 
         <option value="{0}">{0}</option> 
        """.format(i)


	print """</select> 
      <input name="Submit"  type="submit" value="Plot"/>
    </form>
</center>
</tr>
<tr>
 <div id="myDiv">
        <!-- Plotly chart will be drawn inside this DIV -->
 </div>
</tr>
</body>
</html>

"""



