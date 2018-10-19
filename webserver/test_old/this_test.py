#!/usr/bin/python





import json 




def get_all_variables(file_path):
        with open(file_path) as f:
                data = json.load(f)
                return data["body"].keys()



all_variables = get_all_variables("users/JWD88O9VHF38/view_results/view.json")






print "Content-type: text/html"
print 




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


	var xdata = null;
	var ydata = null;
	var xlab = null;
	var ylab = null;
	//var graphtitle = null

	$.getJSON('users/JWD88O9VHF38/view_results/view.json', function(data) {

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
      function handleIt(last_name) {

        alert("hello " + last_name);
      }

    </script>
  </head>
<body>

    <form name="myform" action="javascript:plot_this()">
  <select id="x_var">
	"""

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

 <div id="myDiv">
  	<!-- Plotly chart will be drawn inside this DIV -->
 </div>

</body>
</html>

"""

