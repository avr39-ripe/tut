#!/usr/bin/env python

import tornado.httpclient
import tornado.escape

if __name__ == 'main'
	base_url = 'http://127.0.0.1:8888/'
	request = tornado.web.HTTPRequest(base_url,
					method="POST", 
					headers = {'Content-Type': 'application/json'},
					body = tornado.escape.json_encode({"name": "avr39-ripe", "number": "42" })
	hc = tornado.httpclient.HTTPClient()
	response = hc.fetch(request)
	print response.body
	