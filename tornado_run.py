#coding:utf-8
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from manage import app

# define("port", default=10010, help="run on the given port", type=int)
# define("develop", default=True, help="develop environment", type=bool)

if __name__ == "__main__":
    http_server = HTTPServer(WSGIContainer(app))
    port = '5001'
    http_server.listen(port)    #flask默认的端口
    print("visit at", "http://127.0.0.1:{}".format(port,))
    # tornado.options.parse_command_line()
    IOLoop.instance().start()