import json

from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

MESSAGES = []
COUNT_MSG = 0  # Счетчик сообщений в БД
MSG_REVIEW = {}  # Монитор отправленных сообщений для каждого IP


def save_message(environ):
	global MESSAGES
	global COUNT_MSG
	content_len = int(environ.get('CONTENT_LENGTH',0) or 0)
	req_body = environ['wsgi.input']
	message = req_body.read(content_len).decode('utf-8')
	ip = environ['REMOTE_ADDR']
	MESSAGES.append((ip, message))
	#print(message, COUNT_MSG)
	COUNT_MSG += 1
	return [message.encode()]


def get_message(environ):
	global MESSAGES
	global COUNT_MSG
	global MSG_REVIEW
	if not environ['REMOTE_ADDR'] in MSG_REVIEW:
		MSG_REVIEW[environ['REMOTE_ADDR']] = 0
	to_return = []
	for count in range(MSG_REVIEW[environ['REMOTE_ADDR']], COUNT_MSG):
	#for (ip, message) in MESSAGES:
		if MESSAGES[count][0] != environ['REMOTE_ADDR']:
			to_return.append(MESSAGES[count][1])
	MSG_REVIEW[environ['REMOTE_ADDR']] = COUNT_MSG
	return [json.dumps({'result': to_return}).encode()]


def on_invalid_method(environ):
	return [b'WTF!\n']


def simple_app(environ, start_response):

	setup_testing_defaults(environ)

	status = '200 OK'
	headers = [('Content-Type', 'plain/text'), ('Access-Control-Allow-Origin', '*')]

	start_response(status, headers)

	req_method = environ['REQUEST_METHOD']

	if req_method == 'GET':
		return get_message(environ)
	elif req_method == 'POST':
		return save_message(environ)

	return on_invalid_method(environ)


port = 8000
httpd = make_server('', port, simple_app)
print("Serving on port {0}...".format(port))
httpd.serve_forever()
