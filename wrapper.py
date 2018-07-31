#!/usr/bin/python
import os
import subprocess
import json
os.chdir("/action")
process = subprocess.Popen("/usr/bin/Rscript code.R", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
process.wait()
if os.path.isfile("out.json"):
	with open('out.json') as f:
		data = json.load(f)
		print(json.dumps(data))
else:
	ret = {"msg": "DNE"}
	print(json.dumps(ret))