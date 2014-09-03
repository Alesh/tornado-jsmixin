import logging
import fromtut
import tornado.ioloop


if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG)
    fromtut.Application(debug=True).listen(5000)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()