import os.path
import jsmixin
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    """ Main page handler """
    def get(self):
        self.render("helloworld.html")


class Application(tornado.web.Application, jsmixin.ReactMixin):
    """ Application class """
    def __init__(self, **settings):
        root_path = os.path.dirname(__file__)
        settings.setdefault('template_path', root_path)
        settings.setdefault('static_path', os.path.join(root_path, 'static'))
        tornado.web.Application.__init__(self, [
            (r"/index.html", MainHandler), (r"/", MainHandler)
        ], **settings)
        jsmixin.ReactMixin.__init__(self, **settings)
        #self.registerFile(os.path.join(root_path, 'helloworld.jsx'), 'HelloWorld')
        self.registerFile(os.path.join(root_path, 'helloworld.cjsx'), 'HelloWorld')
        self.buildBundle()


if __name__ == '__main__':
    
    import logging
    import tornado.ioloop
    
    logging.basicConfig(level=logging.DEBUG)
    Application(debug=True).listen(5000)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
