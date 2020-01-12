from . import request, SafeEval, app


@app.route('/compile', methods=['POST', 'GET'])
def compile():
	result = ''
	request_data = request.json
	if request_data:
		if request_data['script'].replace(' ', '') != '':
			lineRes = str(SafeEval.calcuateEval(request_data['script']))
			if lineRes != '' and lineRes != '\n':
				result = lineRes
	else:
		result = "Error: the request data must be json"

	return result


@app.route('/test', methods=['POST', 'GET'])
def test():
	# args = request.args.to_dict()
	return "true"
