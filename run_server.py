#!/usr/bin/env python
# tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
# std lib
import os.path
import logging

# momoko
import momoko
import psycopg2

# application
from app.application import Application
from app.utils.safehttpserver import SafeHTTPServer

# momoko configuration
db_database = os.environ.get('MOMOKO_DB', 'shortlrdb')
db_user = os.environ.get('MOMOKO_USER', 'postgres')
db_password = os.environ.get('MOMOKO_PASSWORD', 'postgres')
db_host = os.environ.get('MOMOKO_HOST', 'localhost')
db_port = os.environ.get('MOMOKO_PORT', 5432)
enable_hstore = True if os.environ.get('MOMOKO_HSTORE', False) == '1' else False
dsn = 'dbname=%s user=%s password=%s host=%s port=%s' % (
    db_database, db_user, db_password, db_host, db_port)

assert (db_database or db_user or db_password or db_host or db_port) is not None, (
    'Environment variables for the examples are not set. Please set the following '
    'variables: MOMOKO_DB, MOMOKO_USER, MOMOKO_PASSWORD, '
    'MOMOKO_HOST, MOMOKO_PORT')


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

    application.db = momoko.Pool(
        dsn=dsn,
        size=1,
        max_size=3,
        ioloop=ioloop,
        raise_connect_errors=False,
        cursor_factory=psycopg2.extras.DictCursor
    )

    # this is a one way to run ioloop in sync
    future = application.db.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()

    if enable_hstore:
        future = application.db.register_hstore()
        # This is the other way to run ioloop in sync
        ioloop.run_sync(lambda: future)

    if application.db.server_version >= 90200:
        future = application.db.register_json()
        # This is the other way to run ioloop in sync
        ioloop.run_sync(lambda: future)

	http_server = SafeHTTPServer(application)
    http_server.listen(options.port)
    logging.info('started on port: %d', options.port)
    ioloop.start()


if __name__ == '__main__':
    main()