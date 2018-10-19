import subprocess
import os


def run_code(action_name, zipname, memory=8000):
    with open("runlogs2.txt", 'w') as f:
        print "Before wsk action..."
        cmd = '/bin/wsk -i action create ' + str(action_name) + ' ' + str(zipname) + ' -m {0} --docker tuna/python-pillow'.format(memory)
        p = subprocess.Popen(cmd, stdout=f, stderr=f, shell=True)
        p.wait()
        print "After wsk action..."

        cmd = 'wsk -i action invoke ' + str(action_name)
        p = subprocess.Popen(cmd, stdout=f, stderr=f, shell=True)
        p.wait()

action_name = "TestNabeel"
zipname = 'code.zip'
memory = 8000

os.system("wsk -i property set --apihost 129.114.109.157")
os.system("wsk -i property get --auth 23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP")

# call function
run_code(action_name, zipname, memory)
