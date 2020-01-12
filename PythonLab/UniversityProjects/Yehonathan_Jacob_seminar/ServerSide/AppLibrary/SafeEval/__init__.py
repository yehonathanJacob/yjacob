# creating a safe dictionary of functions
from math import *
safeDict = locals().copy()
funcs = list(safeDict.keys()).copy()
for key in funcs:
	if key[:2] == "__":
		del safeDict[key]

safeDict['abs'] = abs
safeDict['print'] = print


def get_safe_functions():
	return list(safeDict.keys())


safeDict['safe_functions'] = get_safe_functions

import io
from contextlib import redirect_stdout


def calcuateEval(scriptLine):
	try:
		with io.StringIO() as buf, redirect_stdout(buf):
			exec (compile(scriptLine, '', 'single'), {"__builtins__": {}}, safeDict)
			output = buf.getvalue()
		return output
	except Exception as ex:
		return 'Error: {}\n'.format(str(ex))
