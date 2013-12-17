#!/usr/bin/env python

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
	a =	{'temp': 25.4,
		'delta': 0.25,
		'working_time': 30,
		'working_delta': 5 }
		
        self.write(a)
    def post(self):
	self.write(self.request.body)
	

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
