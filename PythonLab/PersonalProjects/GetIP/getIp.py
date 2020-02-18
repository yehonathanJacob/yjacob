from requests import get
from jinja2 import Template
import argparse
import os

parser = argparse.ArgumentParser(description='Process some data.')
parser.add_argument('--no_print', help="if you don't want to print the ip")
parser.add_argument('--template', help='directory to the tamplate to be render')
parser.add_argument('--resultDir', default='directory to the result')
args = parser.parse_args()

def get_IP():
	ip = get('https://api.ipify.org').text
	return ip

def updateTemplate(templateDir,resultDir,ip):
	if os.path.exists(templateDir):
		path = templateDir
	else:
		path = os.path.join('templates',templateDir)
		if not os.path.exists(path):
			print("Error, template not found")
			return
	with open(path,"r") as f:
		templateTxt = f.read()
		f.close()
	tm = Template(templateTxt)
	data = {'ip':ip}
	msg = tm.render(**data)
	with open(resultDir,"w+") as f:
		f.write(msg)
		f.close()

if __name__ == '__main__':
	ip = get_IP()
	if not args.no_print:
		print(ip)

	if args.template and args.resultDir:
		updateTemplate(args.template, args.resultDir, ip)



