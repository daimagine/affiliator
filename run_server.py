#!/usr/bin/env python
# tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
# std lib
import os.path
import logging

# application
from app.application import Application
from app.utils.safe_httpserver import SafeHTTPServer


# cmd line options
tornado.options.define('port', type=int, default=8080, 
    help='server port number (default: 8080)')
tornado.options.define('debug', type=bool, default=False, 
    help='run in debug mode with autoreload (default: false)')

def main():
    tornado.options.parse_command_line()
    options = tornado.options.options
    application = Application()
    ioloop = tornado.ioloop.IOLoop.instance()

    http_server = SafeHTTPServer(application)
    http_server.listen(options.port)
    logging.info('started on port: %d', options.port)
    ioloop.start()


if __name__ == '__main__':
    main()